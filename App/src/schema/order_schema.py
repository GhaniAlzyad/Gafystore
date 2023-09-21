from pydantic import BaseModel
from datetime import datetime
from App.src.models import Order
from App.src.models import Customer
from . import ProductOrderSchema
from typing import List


class OrderRequestSchema(BaseModel):
    customer_id: str
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
    products: List[ProductOrderSchema]

    class Config:
        orm_mode = True

    @classmethod
    async def from_model(cls, order: Order):
        customer = await Customer.get_by_id(order.customer_id)
        return cls(
            id=order.id,
            name=customer.name
        )