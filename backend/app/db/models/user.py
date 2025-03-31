from typing import TYPE_CHECKING, List
from sqlalchemy import String, BIGINT
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import Model
from ...schemas import UserSchema

if TYPE_CHECKING:
    from .audio import AudioOrm

class UserOrm(Model):
    __tablename__ = "users"

    yandex_id: Mapped[int] = mapped_column(BIGINT, unique=True, nullable=False)
    login: Mapped[str] = mapped_column(String(255), nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)

    # Relationships
    audio_files: Mapped[List["AudioOrm"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def to_pydantic(self) -> UserSchema:
        return UserSchema(
            user_id=str(self.id),
            yandex_id=self.yandex_id,
            login=self.login,
            email=self.email,
        )