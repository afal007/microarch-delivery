import logging
import uuid

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from testcontainers.postgres import PostgresContainer

from app.adapters.out.postgresql.order.order_repository import OrderRepository
from app.core.application.usecases.queries.get_unfinished_orders import GetUnfinishedOrdersHandler, \
    GetUnfinishedOrdersQuery
from app.core.domain.kernel.location import Location
from alembic.config import Config

from app.core.domain.model.order.order import Order


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
async def test_get_unfinished_orders_handler_returns_all(order_repository):
    order1 = Order.create_new(id=uuid.uuid4(), location=Location(x=1, y=1))
    order2 = Order.create_new(id=uuid.uuid4(), location=Location(x=2, y=2))
    order2.assign_courier(uuid.uuid4())

    await order_repository.add(order1)
    await order_repository.add(order2)

    handler = GetUnfinishedOrdersHandler(order_repository=order_repository)
    result = await handler.handle(GetUnfinishedOrdersQuery())

    assert len(result) == 2

    assert result[0].id == order1.id
    assert result[0].location.x == order1.location.x
    assert result[0].location.y == order1.location.y

    assert result[1].id == order2.id
    assert result[1].location.x == order2.location.x
    assert result[1].location.y == order2.location.y
