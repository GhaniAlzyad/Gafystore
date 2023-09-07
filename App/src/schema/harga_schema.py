from pydantic import BaseModel
from datetime import datetime

class HargaRequestSchema(BaseModel):
    jumlah_credit_game : int
    harga : int

    class config:
        orm_mode = True

class HargaResponseSchema(BaseModel):
    id_jumlah: int
    jumlah_credit_game : int
    harga : int
    
    class config:
        orm_mode = True