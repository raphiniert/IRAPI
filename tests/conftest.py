import asyncio
import logging
import pytest

from contextlib import asynccontextmanager
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool
from typing import Generator
from api.core.config import settings

logger = logging.getLogger("irapi")

DATABASE_URL = (
    f"postgresql+asyncpg://{settings.db_user}:{settings.db_password.get_secret_value()}"
    f"@{settings.db_server}:{settings.db_port}/{settings.db_db}"
)

async_engine = create_async_engine(DATABASE_URL, poolclass=NullPool)

TestingSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)


@asynccontextmanager
@pytest.fixture(scope="function")
async def get_testing_session():
    async with TestingSessionLocal() as db:
        try:
            yield db
            # await db.commit()
        except:
            logger.warning("DB operation failed, trying to auto-rollback.")
            await db.rollback()
            raise
        finally:
            await db.close()


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
async def app() -> FastAPI:
    from api import create_app
    from api.db.models import Base

    app = create_app()

    # drop all tables and create new ones
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield app

    # clean up afterwards
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="module")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def async_client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
