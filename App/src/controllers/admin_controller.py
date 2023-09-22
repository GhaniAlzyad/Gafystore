from fastapi import APIRouter, Header
from App.src.schema import AdminResponseSchema, AdminRequestSchema, AdminUpdateSchema
from App.src.models import Admin
from App.src.logics import AdminLogic
from App.src.logics.auth_logic import token_validator


api = APIRouter(
    prefix="/admins",
    tags=["admins"],
)

@api.post("/", response_model=AdminResponseSchema)
async def create_admin(admin: AdminRequestSchema):
    return await AdminLogic.create(admin)

@api.get("/{id}", response_model=AdminResponseSchema)
async def get_admin(id: str, token: str = Header(None)): #add header token for authentication
    auth = await token_validator(token) #add auth
    if auth:
        return await AdminLogic.get_by_id(id, auth.adminname)

@api.get("/",response_model=list[AdminResponseSchema])
async def get_all_admin():
    return await Admin.get_all()

@api.put('/{id}', response_model=AdminResponseSchema)
async def update(admin: AdminUpdateSchema):
    return await AdminLogic.update(admin)

@api.delete('/{id}',response_model=bool)
async def delete (id: str):
    return await AdminLogic.delete(id)
