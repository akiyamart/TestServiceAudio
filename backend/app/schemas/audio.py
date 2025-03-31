from pydantic import BaseModel

from .base import BaseStatus

class AudioSchema(BaseModel):
    file_id: str
    user_id: str
    name: str
    path: str

class AudioInsertSchema(BaseModel):
    id: str 
    user_id: str 
    name: str
    path: str

class AudioDefaultResponse(BaseStatus):
    pass