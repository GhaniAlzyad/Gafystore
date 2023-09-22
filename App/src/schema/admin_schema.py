from pydantic import BaseModel
from typing import Optional

class AdminRequestSchema(BaseModel):
    name: str
    adminname: str
    password: str

    class config:
        orm_mode = True

class AdminUpdateSchema(BaseModel):
    id: str
    name: Optional[str] = None
    adminname: Optional[str] = None
    password: Optional[str] = None

class AdminResponseSchema(BaseModel):
    id: str
    name: str
    adminname: str
