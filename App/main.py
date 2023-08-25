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

    from .src.controllers import user_controller, account_controller, game_controller, price_controller, credit_controller

    @app.get('/health-check')
    async def pong():
        return {'ping':'pong'}
        
    app.include_router(
        user_controller.api,
        prefix="/api/v1"
        )
    return app

    app.include_router(
        account_controller.api,
        prefix="/api/v1"
        )
    return app

    app.include_router(
        game_controller.api,
        prefix="/api/v1"
        )
    return app

    app.include_router(
        price_controller.api,
        prefix="/api/v1"
        )
    return app

    app.include_router(
        credit_controller.api,
        prefix="/api/v1"
        )
    return app


app = init_app()
