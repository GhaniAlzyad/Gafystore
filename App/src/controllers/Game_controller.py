from fastapi import APIRouter
from App.src.schema import GameResponseSchema, GameRequestSchema
from App.src.models import Game
from typing import List


api = APIRouter(
    prefix="/games",
    tags=["games"],
)

@api.post("/", response_model=GameResponseSchema)
async def create_Games(Games: GameRequestSchema):
    Games = await Game.create(**dict(Games))
    return Games

@api.get("/{id}", response_model=GameResponseSchema)
async def get_Games(id: int):
    Games = await Game.get(id)
    return Games

@api.get("/",response_model=list[GameResponseSchema])
async def get_all_Games():
    Games = await Game.get_all()
    return Games

@api.put('/{id}', response_model=GameResponseSchema)
async def update(id: int,Games: GameRequestSchema):
    Games = await Game.update(id,**dict(Games))
    return Games

@api.delete('/{id}',response_model=bool)
async def delete (id: int):
    return await Game.delete(id)