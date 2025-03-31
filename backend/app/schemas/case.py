from pydantic import BaseModel

from .delta import ChangeOnDelta

class CaseInfo(BaseModel):
    condition_field: str
    condition_value: str | int | float
    update_value: float | ChangeOnDelta