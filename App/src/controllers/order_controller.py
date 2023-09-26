from fastapi import APIRouter, Header
from App.src.schema import OrderRequestSchema, OrderResponseSchema, OrderUpdateSchema, OrderDetailReport
from App.src.models import Order, Payment
from App.src.logics import OrderLogic
from App.src.logics import token_validator
from typing import List


api = APIRouter(
    prefix="/order",
    tags=["orders"],
)


@api.post("/", response_model=OrderResponseSchema)
async def create_order(order: OrderRequestSchema, token:str = Header(None)):
    auth = await token_validator(token)
    if auth:
        return await OrderLogic.add_order(order)


@api.get("/{id}", response_model=OrderResponseSchema)
async def get_order(id: int):
    order = await Order.get(id)
    return order


# ganti pakai get_by_user_id
@api.get("/customer/{id}", response_model=List[OrderResponseSchema])
async def get_by_user_id(id: str):
    orders = await Order.get_all_by_user_id(id)
    return orders


@api.put('/{id}', response_model=OrderResponseSchema)
async def update(id: int, order: OrderUpdateSchema):
    order = await Order.update(id, **dict(order))
    return order


@api.delete('/{id}', response_model=bool)
async def delete(id: int):
    return await Order.delete(id)


@api.get("/{id}", response_model=OrderResponseSchema)
async def get_user(id: int):
    order = await Order.get(id)
    result = await OrderResponseSchema.from_model(order)
    return result


@api.get("/details/{id}", response_model=OrderDetailReport)
async def get_order_details(id: int, token:str = Header(None)):
    auth = await token_validator(token)
    if auth:
        result = await OrderLogic.order_details(id, auth)

        return result