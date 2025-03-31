from pydantic import BaseModel

class BaseStatus(BaseModel): 
    status: str