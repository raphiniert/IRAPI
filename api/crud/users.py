import logging

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from api.core.security import get_password_hash
from api.db.models import User
from api import schemes

logger = logging.getLogger("irapi")


async def get_user_by_email(db: AsyncSession, email: str):
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: int):
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_users(db: AsyncSession):
    query = select(User)
    result = await db.execute(query)
    return result.scalars().all()


async def create_user(db: AsyncSession, user: schemes.UserCreate):
    obj_in_data = jsonable_encoder(user)
    obj_in_data["hashed_password"] = get_password_hash(user.password)
    del obj_in_data["password"]
    new_user = User(**obj_in_data)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_user(db: AsyncSession, user: schemes.UserUpdate):
    db_user = await get_user_by_id(db=db, user_id=user.id)
    for field, value in user:
        if field == "password":
            hashed_password = get_password_hash(value)
            setattr(db_user, "hashed_password", hashed_password)
            continue
        setattr(db_user, field, value)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def delete_user(db: AsyncSession, user_id: int):
    db_user = await get_user_by_id(db=db, user_id=user_id)
    await db.delete(db_user)
    await db.commit()
    return db_user
