from App.src.models import User
from App.src.schema import UserRequestSchema, UserUpdateSchema
from App.src.logics import generate_password
from App.src.utils import mapping_null_values
from fastapi import HTTPException, status


class UserLogic:
    @staticmethod
    async def create(obj: UserRequestSchema):
        obj.password = generate_password(obj.password)
        user = await User.create(**dict(obj))

        return user

    @staticmethod
    async def get_by_id(id: str, username: str = None):
        user = await User.get_by_id(id)
        print(f"<user{user.username}")
        if user.username == username:
            return user
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    @staticmethod
    async def update(obj: UserUpdateSchema):
        if obj.password is not None:
            obj.password = generate_password(obj.password)

        user = await User.get_by_id(obj.id)
        user = mapping_null_values(dict(obj), user.__dict__)
        await User.update(user)

        return user

    @staticmethod
    async def delete(id: str):
        await User.delete(id)

        return {"message": "User deleted successfully"}
