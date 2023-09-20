from pydantic import BaseModel
from datetime import datetime

class HargaRequestSchema(BaseModel):
    game_id : int
    jumlah_credit_game : int
    harga : int

    class config:
        orm_mode = True

class HargaResponseSchema(BaseModel):
    id_jumlah: int
    game_id : int
    jumlah_credit_game : int
    harga : int

    class config:
        orm_mode = True