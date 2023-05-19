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


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class UserBase(BaseModel):
    email: str | None = None
    is_active: bool | None = None


class UserDelete(BaseModel):
    message: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserCreate):
    id: int

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    created_at: datetime
    modified_at: datetime
