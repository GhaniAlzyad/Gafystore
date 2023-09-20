from pydantic import BaseModel
from typing import Optional

class addRequestSchema(BaseModel):
    user_id: str
    game_id: int
    akun_id: str
    quantity: int
    status: str

    class Config:
        orm_mode = True

class addUpdateSchema(BaseModel):
    id: int
    user_id: Optional[int] = None
    game_id: Optional[int] = None
    akun_id: Optional[str] = None
    quantity: Optional[int] = None
    status: Optional[str] = None

class addResponseSchema(BaseModel):
    user_id: str
    game_id: int
    akun_id: str
    quantity: int
    status: str

    class Config:
        orm_mode = True
