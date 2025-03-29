import logging
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from testcontainers.postgres import PostgresContainer
from app.adapters.out.postgresql.order.order_repository import OrderRepository
from app.core.domain.model.order.order import Order, OrderStatus
from app.core.domain.kernel.location import Location
from alembic.config import Config


@pytest.fixture(scope="session", autouse=True)
async def logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    yield logger


@pytest.fixture(scope="session")
async def postgres_container(logger):
    logger.info("SETUP postgres testcontainers")
    with PostgresContainer("postgres:16-alpine") as postgres:
        yield postgres


@pytest.fixture(scope="session")
async def database_engine(postgres_container, logger):
    logger.info("SETUP database engine")
    url = postgres_container.get_connection_url(driver='psycopg')
    engine = create_async_engine(url, echo=True)
    return engine


@pytest.fixture(scope="session", autouse=True)
async def alembic_config(postgres_container, logger):
    logger.info("SETUP alembic config")
    cfg = Config("../alembic.ini")
    cfg.set_main_option("script_location", "../alembic")
    cfg.set_main_option("sqlalchemy.url", postgres_container.get_connection_url(driver='psycopg'))
    return cfg


@pytest.fixture(scope="function", autouse=True)
def alembic_run(alembic_runner, logger):
    logger.info("SETUP alembic migration")
    alembic_runner.migrate_up_to("head")
    yield
    alembic_runner.migrate_down_to("base")
    logger.info("TEARDOWN alembic migration")


@pytest.fixture()
async def session_factory(database_engine):
    return async_sessionmaker(bind=database_engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture()
async def order_repository(session_factory):
    return OrderRepository(session_factory)


@pytest.mark.asyncio
async def test_add_and_get_order(order_repository):
    order = Order.create_new(id=uuid4(), location=Location(x=5, y=5))
    await order_repository.add(order)
    retrieved_order = await order_repository.get_by_id(order.id)

    assert retrieved_order is not None
    assert retrieved_order.id == order.id
    assert retrieved_order.location.x == order.location.x
    assert retrieved_order.location.y == order.location.y
    assert retrieved_order.status == order.status


@pytest.mark.asyncio
async def test_update_order(order_repository):
    order = Order.create_new(id=uuid4(), location=Location(x=3, y=3))
    await order_repository.add(order)
    order.assign_courier(uuid4())
    await order_repository.update(order)

    updated_order = await order_repository.get_by_id(order.id)
    assert updated_order.status == OrderStatus.ASSIGNED


@pytest.mark.asyncio
async def test_get_all_new_orders(order_repository):
    order1 = Order.create_new(id=uuid4(), location=Location(x=1, y=1))
    order2 = Order.create_new(id=uuid4(), location=Location(x=2, y=2))
    await order_repository.add(order1)
    await order_repository.add(order2)

    new_orders = await order_repository.get_all_new()
    assert len(new_orders) == 2


@pytest.mark.asyncio
async def test_get_all_assigned_orders(order_repository):
    order1 = Order.create_new(id=uuid4(), location=Location(x=1, y=1))
    order2 = Order.create_new(id=uuid4(), location=Location(x=2, y=2))
    await order_repository.add(order1)
    await order_repository.add(order2)
    order1.assign_courier(uuid4())
    await order_repository.update(order1)

    assigned_orders = await order_repository.get_all_assigned()
    assert len(assigned_orders) == 1
    assert assigned_orders[0].status == OrderStatus.ASSIGNED
