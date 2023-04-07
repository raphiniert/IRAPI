from fastapi import APIRouter

router = APIRouter(
    prefix="/signals",
    tags=["signals"],
    responses={
        400: {"description": "Bad request"},
        404: {"description": "Not found"},
    },
)


@router.get("/")
async def read_signals() -> dict:
    return {"Hello": "World"}
