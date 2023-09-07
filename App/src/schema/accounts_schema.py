from pydantic import BaseModel
from datetime import datetime
from ..models import Account,Game

class AccountRequestSchema(BaseModel):
    game_id : int
    level : int
    items : str

    class config:
        orm_mode = True

class AccountResponseSchema(BaseModel):
    account_id : int
    nama_game: str
    game_id : int
    level : int
    items : str
    date_created : datetime


    @classmethod
    async def from_model(cls, accaount: Account):
        user = await Game.get(accaount.game_id)
        return cls(
            account_id=accaount.account_id,
            game_id=accaount.game_id,
            level=accaount.level,
            items=accaount.items,
            date_created=accaount.date_created,
            nama_game=user.title
        )