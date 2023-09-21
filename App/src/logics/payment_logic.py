from hashlib import sha256
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from App.src.models import Payment, Harga
from App.src.schema import AuthSchema, PaymentRequestSchema

class PaymentLogic:

    @staticmethod
    async def create(obj: PaymentRequestSchema):
        game = await Harga.get(obj.game_id)
        return await Payment.create(**dict(obj))

    @staticmethod
    async def show_items(id: int):
        return await Payment.get_by_game_id(id)