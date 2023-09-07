from pydantic import BaseModel
from datetime import datetime

class GameRequestSchema(BaseModel):
    title : str
    genre : str
    description : str 
    release_date : str

    class config:
        orm_mode = True

class GameResponseSchema(BaseModel):
    game_id: int
    title : str
    genre : str
    description : str 
    release_date : str
    
    class config:
        orm_mode = True