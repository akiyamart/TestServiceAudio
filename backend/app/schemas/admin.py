from pydantic import BaseModel

class AdminSchema(BaseModel):
    admin_id: str
    login: str
    password_hash: str
    created_at: str
