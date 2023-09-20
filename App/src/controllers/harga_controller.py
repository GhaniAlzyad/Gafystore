from fastapi import APIRouter
from App.src.schema import HargaResponseSchema, HargaRequestSchema
from App.src.models import Harga
from App.src.logics import HargaLogic
from typing import List


api = APIRouter(
    prefix="/harga",
    tags=["harga"],
)

@api.post("/", response_model=HargaResponseSchema)
async def create_harga(harga: HargaRequestSchema):
    return await HargaLogic.create(harga)

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

@api.get('/search/', response_model=list[HargaResponseSchema])
async def search(game_id: int or None = ''):
    harga = await Harga.get_by_game_id(game_id)
    return harga
