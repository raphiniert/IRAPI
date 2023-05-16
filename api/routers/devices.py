import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from api import schemas
from api.crud.devices import (
    create_device,
    delete_device,
    get_device,
    get_devices,
    update_device,
)
from api.database import get_db

logger = logging.getLogger("irserver")

router = APIRouter(
    prefix="/devices",
    tags=["devices"],
    responses={
        400: {"description": "Bad request"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "Not found"},
        405: {"description": "Method not Allowed"},
    },
)


@router.get("/", response_model=List[schemas.IRDevice])
async def read_devices(db: AsyncSession = Depends(get_db)) -> List[schemas.IRDevice]:
    devices = await get_devices(db)
    return devices


@router.get("/{device_id}", response_model=schemas.IRDevice)
async def read_device(device_id: int, db: AsyncSession = Depends(get_db)):
    db_device = await get_device(db=db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="IRDevice not found")
    return db_device


@router.post("/", response_model=schemas.IRDevice, status_code=201)
async def create_new_device(
    device: schemas.IRDeviceCreate, db: AsyncSession = Depends(get_db)
):
    return await create_device(db=db, device=device)


@router.patch("/{device_id}", response_model=schemas.IRDevice)
async def patch_device(
    device_id: int, device: schemas.IRDeviceUpdate, db: AsyncSession = Depends(get_db)
):
    if device_id != device.id:
        raise HTTPException(status_code=400, detail="IRDevice id's not matching")
    return await update_device(db=db, device=device)


@router.delete("/{device_id}", response_model=schemas.IRDeviceDelete)
async def remove_device(device_id: int, db: AsyncSession = Depends(get_db)):
    db_device = await delete_device(db=db, device_id=device_id)
    return {"message": f"IRDevice with id: {db_device.id} deleted"}
