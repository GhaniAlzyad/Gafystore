from App.src.models import CartItem
from App.src.schema import addRequestSchema, addResponseSchema
from App.src.logics import generate_password
from App.src.utils import mapping_null_values
from fastapi import HTTPException, status


class AddLogic:
    @staticmethod
    async def create(obj: addRequestSchema, id: str):
       # Lakukan pengecekan apakah item dengan id_jumlah yang sama sudah ada dalam keranjang
        existing_item = await CartItem.get_by_user_and_id_jumlah (id,obj.id_jumlah)
        
        if existing_item:
            # Jika item dengan id_jumlah yang sama sudah ada dalam keranjang,
            # lakukan penambahan jumlahnya
            existing_item.quantity += obj.quantity
            await existing_item.commit()
            return existing_item

        else:
        #     # Jika item belum ada dalam keranjang, tambahkan item baru
        #     param = addResponseSchema(
        #     user_id=id,
        #     id_jumlah=obj.id_jumlah,
        #     account_id=obj.account_id,
        #     quantity=obj.quantity,
        #     status=obj.status,
        #     )
            
            return await CartItem.create(id, **dict(obj))
            

        # # Mapping otomatis objek CartItem ke objek addResponseSchema
        # response_data = addResponseSchema.from_orm(new_item) if not existing_item else addResponseSchema.from_orm(existing_item)

        # return response_data
        # # param = addResponseSchema(
        # #     user_id=id,
        # #     id_jumlah=obj.id_jumlah,
        # #     account_id=obj.account_id,
        # #     quantity=obj.quantity,
        # #     status=obj.status,
        # # )
        # return await CartItem.create(id, **dict(obj))

