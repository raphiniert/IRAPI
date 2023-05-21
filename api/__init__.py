import logging

from fastapi import FastAPI, APIRouter
from rich.logging import RichHandler

from api.core.config import settings
from api.database import async_engine
from api.db.models import Base

FORMAT = "%(message)s"
logging.basicConfig(
    level="DEBUG",
    format=FORMAT,
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[RichHandler()],
)

logger = logging.getLogger("irserver")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Fast API IR Server",
        description="Receive, manage and send infranred signals.",
        version="0.1.0",
    )

    @app.on_event("startup")
    async def startup():
        logger.info("startup")
        async with async_engine.begin() as conn:
            # await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @app.on_event("shutdown")
    async def shutdown():
        logger.info("shutdown")
        await async_engine.dispose()

    router = APIRouter(
        prefix=settings.router_prefix,
    )

    from api.routers import auth, devices, signals, users

    router.include_router(auth.router, prefix=settings.router_version_prefix)
    router.include_router(devices.router, prefix=settings.router_version_prefix)
    router.include_router(signals.router, prefix=settings.router_version_prefix)
    router.include_router(users.router, prefix=settings.router_version_prefix)
    app.include_router(router)

    return app
