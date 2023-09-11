from fastapi import APIRouter
from App.src.schema import AccountRequestSchema,AccountResponseSchema
from App.src.models import Account
from typing import List

api = APIRouter(
    prefix="/account",
    tags=["account"],
)
@api.post("/", response_model=AccountResponseSchema)
async def create_account(account: AccountRequestSchema):
    account = await Account.create(**dict(account))
    return account

# @api.get("/{id}", response_model=AccountResponseSchema)
# async def get_account(id: int):
#     account = await Account.get(id)
#     return account

@api.get("/",response_model=list[AccountResponseSchema])
async def get_all_account():
    account = await Account.get_all()
    return account

@api.put('/{id}', response_model=AccountResponseSchema)
async def update(id: int,account: AccountRequestSchema):
    account = await Account.update(id,**dict(account))
    return account

@api.delete('/{id}',response_model=bool)
async def delete (id: int):
    return await Account.delete(id)

@api.get("/(id)", response_model=AccountResponseSchema)
async def get_Account(id:int):
    barang = await Account.get(id)
    result = await AccountResponseSchema.from_model(barang)
    return result