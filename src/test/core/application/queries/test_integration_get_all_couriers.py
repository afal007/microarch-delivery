import logging

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from testcontainers.postgres import PostgresContainer

from app.adapters.out.postgresql.courier.courier_repository import CourierRepository
from app.core.application.usecases.queries.get_all_couriers import GetAllCouriersHandler, GetAllCouriersQuery
from app.core.domain.model.courier.courier import Courier, TransportParams
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
async def test_get_all_couriers_integration(courier_repository):
    courier1 = Courier.create(
        name="Alex",
        transport_params=TransportParams(name="bike", speed=2),
        location=Location(x=1, y=1)
    )
    courier2 = Courier.create(
        name="Lena",
        transport_params=TransportParams(name="car", speed=3),
        location=Location(x=5, y=7)
    )
    await courier_repository.add(courier1)
    await courier_repository.add(courier2)

    handler = GetAllCouriersHandler(courier_repository=courier_repository)
    result = await handler.handle(GetAllCouriersQuery())

    assert len(result) == 2

    assert result[0].id == courier1.id
    assert result[0].name == courier1.name
    assert result[0].location.x == courier1.location.x
    assert result[0].location.y == courier1.location.y

    assert result[1].id == courier2.id
    assert result[1].name == courier2.name
    assert result[1].location.x == courier2.location.x
    assert result[1].location.y == courier2.location.y
