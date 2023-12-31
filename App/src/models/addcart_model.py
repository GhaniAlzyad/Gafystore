from sqlalchemy import  Column, Integer, String
from sqlalchemy import false, true
from sqlalchemy import delete as sqlalchemy_delete, update as sqlalchemy_update
from sqlalchemy.orm import relationship
from sqlalchemy import select
from ...database import base, db
from datetime import datetime
from fastapi import HTTPException, status

class CartItem(base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    id_jumlah = Column(Integer)
    account_id =Column(Integer)
    quantity = Column(Integer, default=1)
    status = Column(String, nullable=False) #paid / unpaid

    def __repr__(self):
        return f"<user_id)"


    @classmethod
    async def create(cls,id, **kwargs):
        CartItem = cls(user_id=id, **kwargs)
        db.add(CartItem)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return CartItem

    @classmethod
    async def get_by_id(cls, id):
        query = select(cls).where(cls.CartItem_id == id)
        cart_items = await db.execute(query)
        (CartItem,)= cart_items.first()
        return CartItem
    
    @classmethod
    async def get_by_user_and_id_jumlah(cls, user_id,id_jumlah):
        query = select(cls).where(cls.user_id==user_id,cls.id_jumlah==id_jumlah)
        cart_items = await db.execute(query)

        return cart_items.scalar_one_or_none()

    @classmethod
    async def get_all(cls):
        query=select(cls)
        cart_items =await db.execute(query)
        cart_items = cart_items.scalars().all()
        return cart_items

    @classmethod
    async def update(cls,id,**kwargs):
        CartItem = await cls.get(id)
        CartItem.from_dict(kwargs)

        CartItem_dict =CartItem.__dict__
        CartItem_dict.pop("_sa_instance_state",None)

        query =(
            sqlalchemy_update(cls)
            .where(cls.id == id)
            .values(**CartItem_dict)
            .execution_options(synchronize_session=False)
        )

        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise

        return CartItem_dict
    @classmethod
    async def delete(cls, id):
        query = sqlalchemy_delete(cls).where(cls.id == id)
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return True

    def from_dict(self, data):
        fields=[
            'user_id', 'game_id', 'amount', 'purchase_date', 'metode_pembayaran', 'status_pembayaran',
        ]
        for field in fields:
            value = data.get(field)
            if value is not None:
                setattr(self, field, value)
    @staticmethod
    async def commit():
        try:
            await db.commit()
        except:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")