from fastapi import APIRouter, status
from App.src.logics import AuthLogic
from App.src.schema import AuthSchema


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/login", status_code=status.HTTP_200_OK)
async def login(param: AuthSchema):
    return await AuthLogic.login(param)
