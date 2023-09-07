from pydantic import BaseModel
from datetime import datetime

class CreditsRequestSchema(BaseModel):
    user_id : int
    game_id : int
    amount : int 
    metode_pembayaran : str
    status_pembayaran :str

    class config:
        orm_mode = True

class CreditsResponseSchema(BaseModel):
    credit_id : int
    user_id : int
    game_id : int
    amount : int 
    purchase_date : datetime
    metode_pembayaran : str
    status_pembayaran :str
    
    class config:
        orm_mode = True