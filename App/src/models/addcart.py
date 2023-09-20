from sqlalchemy import  Column, Integer, String
from sqlalchemy import false, true 
from sqlalchemy import delete as sqlalchemy_delete, update as sqlalchemy_update
from sqlalchemy.orm import relationship
from sqlalchemy import select
from ...database import base, db
from datetime import datetime



class CartItem(base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    game_id = Column(Integer)
    account_id =Column(Integer)
    quantity = Column(Integer, default=1)
    token = Column(String(255), nullable=True)
    status = Column(String, nullable=False) #paid / unpaid

    def __repr__(self):
        return f"<user_id)"
    
        
    @classmethod
    async def create(cls,**kwargs):
        CartItem = cls(**kwargs)
        db.add(CartItem)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return CartItem
    
    @classmethod
    async def get(cls, id):
        query = select(cls).where(cls.CartItem_id == id)
        cart_items = await db.execute(query)
        (CartItem,)= cart_items.first()
        return CartItem
    
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