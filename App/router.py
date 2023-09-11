from .src.controllers import user_controller, Game_controller,credits_controller,accounts_controller,accounts_controller,auth_controller
from fastapi import APIRouter


api = APIRouter()

@api.get("/health-check")
async def health_check():
    return {"message": "Health Check"}

api.include_router(user_controller.api)
api.include_router(Game_controller.api)
api.include_router(credits_controller.api)
api.include_router(accounts_controller.api)
api.include_router(accounts_controller.api)
api.include_router(auth_controller.router)