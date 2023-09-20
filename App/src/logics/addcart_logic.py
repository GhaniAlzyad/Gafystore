from App.src.models import CartItem
from App.src.schema import addRequestSchema, addUpdateSchema
from App.src.logics import generate_password
from App.src.utils import mapping_null_values
from fastapi import HTTPException, status


class AddLogic:
    @staticmethod
    async def create(obj: addRequestSchema, id: str):
        obj.id = id
        return await CartItem.create(**dict(obj))

