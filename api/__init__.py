from fastapi import FastAPI, APIRouter


def create_app() -> FastAPI:
    app = FastAPI(
        title="Fast API IR Server",
        description="Receive, manage and send infranred signals.",
        version="0.1.0",
    )

    router = APIRouter(
        prefix="/api",
    )

    from api.routers import signals

    router.include_router(signals.router, prefix="/v1")
    app.include_router(router)

    return app
