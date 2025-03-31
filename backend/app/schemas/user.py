from pydantic import BaseModel

from .base import BaseStatus

class UserSchema(BaseModel):
    user_id: str
    yandex_id: int
    login: str
    email: str

class UserInsertSchema(BaseModel): 
    yandex_id: int 
    login: str
    email: str

class UserUpdate(BaseModel): 
    login: str | None = None
    email: str | None = None

class UserDefaultResponse(BaseStatus):
    pass