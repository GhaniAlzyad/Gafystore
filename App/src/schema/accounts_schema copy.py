from pydantic import BaseModel
from datetime import datetime
from ..models import Account,Game

class AccountRequestSchema(BaseModel):
    game_id : int
    level : int
    items : str
    date_created : datetime

    class config:
        orm_mode = True

class AccountResponseSchema(BaseModel):
    account_id : int
    game_id : int
    level : int
    items : str
    date_created : datetime

    class config:
        orm_mode = True


    @classmethod
    async def from_model(cls, accaount: Account):
        user = await Game.get(accaount.game_id)
        return cls(
            id=accaount.account_id,
            nama_game=user.title
        )