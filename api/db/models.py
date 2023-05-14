from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, func, Integer
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
    relationship,
)
from typing import List

# from api.database import Base


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class IRDevice(Base):
    # Table settings
    __tablename__ = "devices"

    # Columns
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    signals: Mapped[List["IRSignal"]] = relationship(
        back_populates="device", default_factory=list, lazy="selectin"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=func.now()
    )
    modified_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now()
    )


class IRSignal(Base):
    # Table settings
    __tablename__ = "signals"

    # Columns
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    signal: Mapped[List[List[int]]] = mapped_column(
        postgresql.ARRAY(Integer, dimensions=2), nullable=False
    )
    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"), nullable=True)
    device: Mapped["IRDevice"] = relationship(back_populates="signals", default=None)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=func.now()
    )
    modified_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now()
    )
