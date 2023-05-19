from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from api import schemes
from api.crud.signals import (
    create_signal,
    delete_signal,
    get_signal,
    get_signals,
    update_signal,
)
from api.database import get_db

router = APIRouter(
    prefix="/signals",
    tags=["signals"],
    responses={
        400: {"description": "Bad request"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "Not found"},
        405: {"description": "Method not Allowed"},
    },
)


@router.get("/", response_model=List[schemes.IRSignal])
async def read_signals(db: AsyncSession = Depends(get_db)) -> List:
    signals = await get_signals(db)
    return signals


@router.get("/{signal_id}", response_model=schemes.IRSignal)
async def read_signal(signal_id: int, db: AsyncSession = Depends(get_db)):
    db_signal = await get_signal(db=db, signal_id=signal_id)
    if db_signal is None:
        raise HTTPException(status_code=404, detail="IRSignal not found")
    return db_signal


@router.post("/", response_model=schemes.IRSignal, status_code=201)
async def create_new_signal(
    signal: schemes.IRSignalCreate, db: AsyncSession = Depends(get_db)
):
    return await create_signal(db=db, signal=signal)


@router.patch("/{signal_id}", response_model=schemes.IRSignal)
async def patch_signal(
    signal_id: int, signal: schemes.IRSignal, db: AsyncSession = Depends(get_db)
):
    if signal_id != signal.id:
        raise HTTPException(status_code=400, detail="IRSignal id's not matching")
    return await update_signal(db=db, signal=signal)


@router.delete("/{signal_id}", response_model=schemes.IRSignalDelete)
async def remove_signal(signal_id: int, db: AsyncSession = Depends(get_db)):
    db_signal = await delete_signal(db=db, signal_id=signal_id)
    return {"message": f"IRSignal with id: {db_signal.id} deleted"}
