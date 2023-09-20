from fastapi import APIRouter, Header
from App.src.schema import addResponseSchema, addRequestSchema, addUpdateSchema
from App.src.models import CartItem
from App.src.logics import AddLogic
from App.src.logics.auth_logic import token_validator


api = APIRouter(
    prefix="/adds",
    tags=["adds"],
)

@api.post("/", response_model=addResponseSchema)
async def add_cart(add: addRequestSchema, token: str = Header(None)):
    auth = token_validator(token)
    if auth:
        print(f"<user{auth.id}")
        return await AddLogic.create(add, auth.id)

@api.get("/{id}", response_model=addResponseSchema)
async def get_user(user_id: str, token: str = Header(None)): #add header token for authentication
    auth = await token_validator(token) #add auth
    if auth:
        return await AddLogic.get_by_id(id, auth.user_id)

@api.get("/",response_model=list[addResponseSchema])
async def get_all_user():
    return await CartItem.get_all()

@api.put('/{id}', response_model=addResponseSchema)
async def update(add: addUpdateSchema):
    return await AddLogic.update(add)

@api.delete('/{id}',response_model=bool)
async def delete (id: str):
    return await AddLogic.delete(id)
