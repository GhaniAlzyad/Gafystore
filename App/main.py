from fastapi import FastAPI
from .database import db

def init_app():
    db.init()
    app = FastAPI(
        tittle="website gafystore",
        descriptions="toko credit game online",
        version="1"
    )
    @app.on_event("startup")
    async def startup():
        await db.create_all()
    @app.on_event("shutdown")
    async def shutdown():
        await db.close()

    from .src.controllers import user_controller

    @app.get('/health-check')
    async def pong():
        return {'ping':'pong'}
        
    app.include_router(
        user_controller.api,
        prefix="/api/v1"
        )
    return app

app = init_app()
