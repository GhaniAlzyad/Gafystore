from pydantic import BaseModel
from typing import Optional

class UserRequestSchema(BaseModel):
    name: str
    email: str
    username: str
    password: str

    class config:
        orm_mode = True

class UserUpdateSchema(BaseModel):
    id: str
    name: Optional[str] = None
    email: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None

class UserResponseSchema(BaseModel):
    id: str
    name: str
    email: str
    username: str
