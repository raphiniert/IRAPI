from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from api.core.config import settings


DATABASE_URL = (
    f"postgresql+asyncpg://{settings.db_user}:{settings.db_password.get_secret_value()}"
    f"@{settings.db_server}:{settings.db_port}/{settings.db_db}"
)

# https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#using-multiple-asyncio-event-loops
async_engine = create_async_engine(DATABASE_URL, poolclass=NullPool)

AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as db:
        yield db
        await db.commit()
