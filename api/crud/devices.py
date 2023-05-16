import logging

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from api.db.models import IRDevice
from api import schemas

logger = logging.getLogger("irserver")


async def get_device(db: AsyncSession, device_id: int):
    query = select(IRDevice).where(IRDevice.id == device_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_devices(db: AsyncSession):
    query = select(IRDevice)
    result = await db.execute(query)
    return result.scalars().all()


async def create_device(db: AsyncSession, device: schemas.IRDeviceCreate):
    obj_in_data = jsonable_encoder(device)
    new_device = IRDevice(**obj_in_data)
    db.add(new_device)
    await db.commit()
    await db.refresh(new_device)
    return new_device


async def update_device(db: AsyncSession, device: schemas.IRDeviceUpdate):
    db_device = await get_device(db=db, device_id=device.id)
    for field, value in device:
        setattr(db_device, field, value)
    db.add(db_device)
    await db.commit()
    await db.refresh(db_device)
    return db_device


async def delete_device(db: AsyncSession, device_id: int):
    db_device = await get_device(db=db, device_id=device_id)
    await db.delete(db_device)
    await db.commit()
    return db_device
