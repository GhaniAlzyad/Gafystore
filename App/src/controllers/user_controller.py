from fastapi import APIRouter
from ..schema import UserResponseSchema, UserRequestSchema, LoginSchema
from ..models import User
from typing import List


api = APIRouter(
    prefix="/users",
    tags=["users"],
)

@api.post("/", response_model=UserResponseSchema)
async def create_user(user: UserRequestSchema):
    user = await User.create(**dict(user))
    return user

@api.get("/{id}", response_model=UserResponseSchema)
async def get_user(id: int):
    user = await User.get(id)
    return user

@api.get("/",response_model=list[UserResponseSchema])
async def get_all_user():
    users = await User.get_all()
    return users

@api.put('/{id}', response_model=UserResponseSchema)
async def update(id: int,user: UserRequestSchema):
    user = await User.update(id,**dict(user))
    return user

@api.delete('/{id}',response_model=bool)
async def delete (id: int):
    return await User.delete(id)

@api.post('/login',response_model=bool)
async def login(login: LoginSchema):
    login = await User.login(login)

    if login is not None:
        token = await User.generate_token()
        
        return True
    
    return False