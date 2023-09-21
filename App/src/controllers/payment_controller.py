from fastapi import APIRouter
from App.src.schema import PaymentRequestSchema, PaymentResponseSchema, PaymentUpdateSchema
from App.src.models import Payment
from App.src.logics import PaymentLogic
from typing import List


api = APIRouter(
    prefix="/payment",
    tags=["payments"],
)

@api.post("/", response_model=PaymentResponseSchema)
async def create_payment(payment: PaymentRequestSchema):
    return await PaymentLogic.create_payment(payment)


@api.get("/{id}", response_model=PaymentResponseSchema)
async def get_payment(id: int):
    payment = await Payment.get(id)
    return payment


@api.get("/", response_model=List[PaymentResponseSchema])
async def get_all_payments():
    payments = await Payment.get_all()
    return payments


@api.put('/{id}', response_model=PaymentResponseSchema)
async def update(id: int, payment: PaymentUpdateSchema):
    payment = await Payment.update(id, **dict(payment))
    return payment


@api.delete('/{id}', response_model=bool)
async def delete(id: int):
    return await Payment.delete(id)