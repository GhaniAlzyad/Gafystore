from App.src.models import Harga, Game
from App.src.schema import UserRequestSchema, UserUpdateSchema, HargaRequestSchema
from App.src.logics import generate_password
from App.src.utils import mapping_null_values
from fastapi import HTTPException, status


class HargaLogic:
    @staticmethod
    async def create(obj: HargaRequestSchema):
        game = await Game.get(obj.game_id)
        return await Harga.create(**dict(obj))

    @staticmethod
    async def show_items(id: int):
        return await Harga.get_by_game_id(id)