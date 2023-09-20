from App.src.models import CartItem
from App.src.schema import addRequestSchema, addUpdateSchema
from App.src.logics import generate_password
from App.src.utils import mapping_null_values
from fastapi import HTTPException, status


class AddLogic:
    @staticmethod
    async def create(obj: addRequestSchema):
        obj.password = generate_password(obj.password)
        add = await CartItem.create(**dict(obj))

        return add

    @staticmethod
    async def get_by_id(user_id: str, game_id: int = None):
        add = await CartItem.get_by_id(game_id)
        print(f"<add{add.game_id}")
        if add.game_id == game_id:
            return add
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    @staticmethod
    async def update(obj: addUpdateSchema):
        if obj.password is not None:
            obj.password = generate_password(obj.password)

        add = await CartItem.get_by_id(obj.id)
        add = mapping_null_values(dict(obj), add.__dict__)
        await CartItem.update(add)

        return add

    @staticmethod
    async def delete(game_id: int):
        await CartItem.delete(game_id)

        return {"message": "User deleted successfully"}
