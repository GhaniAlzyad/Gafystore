from fastapi import APIRouter
from ..schema import CreditsResponseSchema, CreditsRequestSchema
from ..models import Credit
from typing import List


api = APIRouter(
    prefix="/credits",
    tags=["credits"],
)

@api.post("/", response_model=CreditsResponseSchema)
async def create_credits(credits: CreditsRequestSchema):
    print(f"<credit({credits})")
    credits = await Credit.create(**dict(credits))
    return credits

@api.get("/{id}", response_model=CreditsResponseSchema)
async def get_credits(id: int):
    credits = await Credit.get(id)
    return credits

@api.get("/",response_model=list[CreditsResponseSchema])
async def get_all_credits():
    credits = await Credit.get_all()
    return credits

@api.put('/{id}', response_model=CreditsResponseSchema)
async def update(id: int,credits: CreditsRequestSchema):
    credits = await Credit.update(id,**dict(credits))
    return credits

@api.delete('/{id}',response_model=bool)
async def delete (id: int):
    return await Credit.delete(id)