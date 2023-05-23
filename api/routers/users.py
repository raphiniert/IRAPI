import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List

from api import schemes
from api.crud.users import (
    create_user,
    delete_user,
    get_user_by_id,
    get_users,
    update_user,
)
from api.db import get_db
from api.routers.auth import get_current_active_user

logger = logging.getLogger("irapi")

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={
        400: {"description": "Bad request"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "Not found"},
        405: {"description": "Method not Allowed"},
        422: {"description": "Unprocessable Entity"},
    },
)


@router.get("/profile", response_model=schemes.User)
async def read_users_me(
    current_user: Annotated[schemes.User, Depends(get_current_active_user)]
):
    return current_user


@router.get("/", response_model=List[schemes.User])
async def read_users(
    current_user: Annotated[schemes.User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> List:
    users = await get_users(db)
    return users


@router.get("/{user_id}", response_model=schemes.User)
async def read_user(
    user_id: int,
    current_user: Annotated[schemes.User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    db_user = await get_user_by_id(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/", response_model=schemes.User, status_code=201)
async def create_new_user(
    user: schemes.UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await create_user(db=db, user=user)


@router.patch("/{user_id}", response_model=schemes.User)
async def patch_user(
    user_id: int,
    user: schemes.UserUpdate,
    current_user: Annotated[schemes.User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    if user_id != user.id:
        raise HTTPException(status_code=400, detail="User id's not matching")
    return await update_user(db=db, user=user)


@router.delete("/{user_id}", response_model=schemes.UserDelete)
async def remove_user(
    user_id: int,
    current_user: Annotated[schemes.User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    db_user = await delete_user(db=db, user_id=user_id)
    return {"message": f"User with id: {db_user.id} deleted"}
