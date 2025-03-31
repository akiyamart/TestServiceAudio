from sqlalchemy.orm import Mapped, mapped_column

from .base import Model
from ...schemas import AdminSchema

class AdminOrm(Model):
    __tablename__ = "admins"
    
    login: Mapped[str] = mapped_column(nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)

    def to_pydantic(self) -> AdminSchema:
        return AdminSchema(
            admin_id=str(self.id),
            login=self.login,
            password_hash=self.password_hash,
            created_at=self.created_at.isoformat(),
        )