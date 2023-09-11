from fastapi import APIRouter, Header
from App.src.schema import UserResponseSchema, UserRequestSchema, UserUpdateSchema
from App.src.models import User
from App.src.logics import UserLogic
from App.src.logics.auth_logic import token_validator


api = APIRouter(
    prefix="/users",
    tags=["users"],
)

@api.post("/", response_model=UserResponseSchema)
async def create_user(user: UserRequestSchema):
    return await UserLogic.create(user)

@api.get("/{id}", response_model=UserResponseSchema)
async def get_user(id: str, token: str = Header(None)):
    auth = await token_validator(token)
    if auth:
        return await UserLogic.get_by_id(id, auth.username)

@api.get("/",response_model=list[UserResponseSchema])
async def get_all_user():
    return await User.get_all()

@api.put('/{id}', response_model=UserResponseSchema)
async def update(user: UserUpdateSchema):
    return await UserLogic.update(user)

@api.delete('/{id}',response_model=bool)
async def delete (id: str):
    return await UserLogic.delete(id)
