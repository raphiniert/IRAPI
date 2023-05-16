import logging

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from api.db.models import IRSignal
from api import schemes

logger = logging.getLogger("irserver")


async def get_signal(db: AsyncSession, signal_id: int):
    query = select(IRSignal).where(IRSignal.id == signal_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_signals(db: AsyncSession):
    query = select(IRSignal)
    result = await db.execute(query)
    return result.scalars().all()


async def create_signal(db: AsyncSession, signal: schemes.IRSignalCreate):
    obj_in_data = jsonable_encoder(signal)
    new_signal = IRSignal(**obj_in_data)
    db.add(new_signal)
    await db.commit()
    await db.refresh(new_signal)
    return new_signal


async def update_signal(db: AsyncSession, signal: schemes.IRSignal):
    db_signal = await get_signal(db=db, signal_id=signal.id)
    for field, value in signal:
        setattr(db_signal, field, value)
    db.add(db_signal)
    await db.commit()
    await db.refresh(db_signal)
    return db_signal


async def delete_signal(db: AsyncSession, signal_id: int):
    db_signal = await get_signal(db=db, signal_id=signal_id)
    await db.delete(db_signal)
    await db.commit()
    return db_signal
