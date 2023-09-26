from pydantic import BaseModel
from datetime import datetime
from App.src.models import Order
from App.src.models import User
from typing import List


class OrderdetailRequestSchema(BaseModel):
    id: str
    # date: datetime
    # order_status: str
    # total_price: float

    class Config:
        orm_mode = True


class OrderdetailUpdateSchema(BaseModel):
    order_status: str

    class Config:
        orm_mode = True


class OrderdetailResponseSchema(BaseModel):
    id: int
    id: str
    date: datetime
    order_status: str
    total_price: float

    class Config:
        orm_mode = True

    @classmethod
    async def from_model(cls, order: Order):
        id = await id.get_by_id(order.id)
        return cls(
            id=order.id,
            name=id.name
        )