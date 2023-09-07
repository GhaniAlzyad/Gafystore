from fastapi import APIRouter
from ..schema import HargaResponseSchema, HargaRequestSchema
from ..models import Harga
from typing import List


api = APIRouter(
    prefix="/harga",
    tags=["harga"],
)

@api.post("/", response_model=HargaResponseSchema)
async def create_harga(harga: HargaRequestSchema):
    harga = await Harga.create(**dict(harga))
    return harga

@api.get("/{id}", response_model=HargaResponseSchema)
async def get_harga(id: int):
    harga = await Harga.get(id)
    return harga

@api.get("/",response_model=list[HargaResponseSchema])
async def get_all_harga():
    harga = await Harga.get_all()
    return harga

@api.put('/{id}', response_model=HargaResponseSchema)
async def update(id: int,harga: HargaRequestSchema):
    harga = await Harga.update(id,**dict(harga))
    return harga

@api.delete('/{id}',response_model=bool)
async def delete (id: int):
    return await Harga.delete(id)