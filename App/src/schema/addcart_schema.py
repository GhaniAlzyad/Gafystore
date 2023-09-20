from pydantic import BaseModel
from typing import Optional

class addRequestSchema(BaseModel):
    id_jumlah: int
    account_id: int
    quantity: int
    status: str

    class Config:
        orm_mode = True

class addUpdateSchema(BaseModel):
    id: int
    user_id: Optional[int] = None
    id_jumlah: Optional[int] = None
    account_id: Optional[int] = None
    quantity: Optional[int] = None
    status: Optional[str] = None

class addResponseSchema(BaseModel):
    user_id: str
    id_jumlah: int
    account_id: int
    quantity: int
    status: str

    class Config:
        orm_mode = True
