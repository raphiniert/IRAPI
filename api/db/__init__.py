import logging

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.pool import NullPool

from api.core.config import settings

logger = logging.getLogger("irapi")

DATABASE_URL = (
    f"postgresql+asyncpg://{settings.db_user}:{settings.db_password.get_secret_value()}"
    f"@{settings.db_server}:{settings.db_port}/{settings.db_db}"
)

# https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#using-multiple-asyncio-event-loops
async_engine = create_async_engine(DATABASE_URL, poolclass=NullPool)

AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as db:
        try:
            yield db
            # await db.commit()
        except:
            logger.warning("DB operation failed, trying to auto-rollback.")
            await db.rollback()
            raise
        finally:
            await db.close()
