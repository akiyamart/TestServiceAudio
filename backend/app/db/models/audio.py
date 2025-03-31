import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from pydantic import BaseModel

from .base import Model
from ...schemas import AudioSchema

if TYPE_CHECKING:
    from .user import UserOrm

class AudioOrm(Model):
    __tablename__ = "audio_files"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    path: Mapped[str] = mapped_column(Text, nullable=False)

    # Relationships
    user: Mapped["UserOrm"] = relationship(back_populates="audio_files")

    def to_pydantic(self) -> BaseModel:
        return AudioSchema( 
            file_id=str(self.id), 
            user_id=str(self.user_id), 
            name=self.name, 
            path=self.path,
        )
