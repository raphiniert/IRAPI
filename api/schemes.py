from datetime import datetime
from pydantic import BaseModel
from typing import List


class IRDeviceDelete(BaseModel):
    message: str


class IRDeviceBase(BaseModel):
    name: str
    signals: List | None = []


class IRDeviceCreate(IRDeviceBase):
    pass


class IRDeviceUpdate(IRDeviceBase):
    id: int

    class Config:
        orm_mode = True


class IRDevice(IRDeviceUpdate):
    created_at: datetime
    modified_at: datetime


class IRSignalDelete(BaseModel):
    message: str


class IRSignalBase(BaseModel):
    name: str
    signal: List[List[int]]
    device_id: int | None = None


class IRSignalCreate(IRSignalBase):
    pass


class IRSignalUpdate(IRSignalBase):
    id: int

    class Config:
        orm_mode = True


class IRSignal(IRSignalUpdate):
    created_at: datetime
    modified_at: datetime
