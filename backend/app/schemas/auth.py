from pydantic import BaseModel

from .base import BaseStatus

class LoginResponse(BaseStatus):
    pass

class TokenData(BaseModel): 
    access_token: str
    refresh_token: str
