from pydantic import BaseModel

class ChangeOnDelta(BaseModel):
    delta: float