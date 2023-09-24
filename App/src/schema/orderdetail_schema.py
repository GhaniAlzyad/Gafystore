from pydantic import BaseModel
from datetime import datetime
from App.src.models import Order
from App.src.models import Customer
from . import ProductOrderSchema
from typing import List


class OrderRequestSchema(BaseModel):
    user_id: str
    # date: datetime
    # order_status: str
    # total_price: float

    class Config:
        orm_mode = True


class OrderUpdateSchema(BaseModel):
    order_status: str

    class Config:
        orm_mode = True


class OrderResponseSchema(BaseModel):
    id: int
    user_id: str
    date: datetime
    order_status: str
    total_price: float
    : List[ProductOrderSchema]

    class Config:
        orm_mode = True

    @classmethod
    async def from_model(cls, order: Order):
        user_id = await user_id.get_by_id(order.user_id)
        return cls(
            id=order.id,
            name=user_id.name
        )