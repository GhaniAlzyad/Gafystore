from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PaymentRequestSchema(BaseModel):
    id_order: int
    method: str
    payment_status: str

    class Config:
        orm_mode = True


class PaymentUpdateSchema(BaseModel):
    method: Optional[str]
    payment_status: Optional[str]


class PaymentResponseSchema(BaseModel):
    id: int
    id_order: int
    method: str
    payment_status: str

    class Config:
        orm_mode=True