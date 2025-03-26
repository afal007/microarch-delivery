import pytest
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from testcontainers.postgres import PostgresContainer

from app.adapters.out.postgresql.courier.courier_repository import CourierRepository
from app.core.domain.model.courier.courier import Courier, CourierStatus, TransportParams
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
async def courier_repository(session_factory):
    return CourierRepository(session_factory)


@pytest.mark.asyncio
async def test_add_and_get_courier(courier_repository):
    courier = Courier.create(
        name="Ivan",
        transport_params=TransportParams(name="bike", speed=2),
        location=Location(x=1, y=1)
    )
    await courier_repository.add(courier)
    result = await courier_repository.get_by_id(courier.id)

    assert result is not None
    assert result.name == "Ivan"
    assert result.transport.name == "bike"
    assert result.transport.speed == 2
    assert result.location.x == 1
    assert result.location.y == 1
    assert result.status == CourierStatus.FREE


@pytest.mark.asyncio
async def test_update_courier(courier_repository):
    courier = Courier.create(
        name="Petr",
        transport_params=TransportParams(name="car", speed=3),
        location=Location(x=2, y=2)
    )
    await courier_repository.add(courier)
    courier.set_status_busy()
    await courier_repository.update(courier)
    updated = await courier_repository.get_by_id(courier.id)

    assert updated.status == CourierStatus.BUSY


@pytest.mark.asyncio
async def test_get_all_free_couriers(courier_repository):
    courier1 = Courier.create(
        name="Courier1",
        transport_params=TransportParams(name="scooter", speed=1),
        location=Location(x=3, y=3)
    )
    courier2 = Courier.create(
        name="Courier2",
        transport_params=TransportParams(name="van", speed=3),
        location=Location(x=4, y=4)
    )
    await courier_repository.add(courier1)
    await courier_repository.add(courier2)

    courier2.set_status_busy()
    await courier_repository.update(courier2)

    free_couriers = await courier_repository.get_all_free()

    assert any(c.id == courier1.id for c in free_couriers)
    assert all(c.status == CourierStatus.FREE for c in free_couriers)
    assert all(c.id != courier2.id for c in free_couriers)
