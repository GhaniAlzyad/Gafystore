from App.src.models import CartItem
from App.src.schema import addRequestSchema, addResponseSchema
from App.src.logics import generate_password
from App.src.utils import mapping_null_values
from fastapi import HTTPException, status


class AddLogic:
    @staticmethod
    async def create(obj: addRequestSchema, id: str):
        # lakukann pengecekan apabila id_jumlah yang sama sudah ditambahkan,
        # jika ada maka lakukan penambahan
        # contoh
        # (id = 5, qty = 10) data yang sudah ada
        # add cart (id = 5, qty = 2)
        # jika ada maka di jumlah 10 + 2
        # param = addResponseSchema(
        #     user_id=id,
        #     id_jumlah=obj.id_jumlah,
        #     account_id=obj.account_id,
        #     quantity=obj.quantity,
        #     status=obj.status,
        # )
        return await CartItem.create(id, **dict(obj))

