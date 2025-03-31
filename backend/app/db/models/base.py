import uuid
import datetime

from sqlalchemy import UUID, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase
from pydantic import BaseModel


class Model(DeclarativeBase):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        doc="Unique ID of the record in table",
        default=uuid.uuid4
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    
    def to_pydantic(self) -> BaseModel:
        pass

    