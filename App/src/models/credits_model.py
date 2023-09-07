from sqlalchemy import  Column, Integer, BigInteger, String, DateTime 
from sqlalchemy import false, true 
from sqlalchemy import delete as sqlalchemy_delete, update as sqlalchemy_update
from sqlalchemy import select
from ...database import base, db
from datetime import datetime


class Credit(base):
    __tablename__ = 'credits'

    credit_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    game_id = Column(Integer)
    amount = Column(Integer)
    purchase_date = Column(DateTime, default=datetime.utcnow)
    metode_pembayaran = Column(String(255), nullable=False)
    status_pembayaran = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<user_id)"
    
        
    @classmethod
    async def create(cls,**kwargs):
        Credit = cls(**kwargs)
        db.add(Credit)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return Credit
    
    @classmethod
    async def get(cls, id):
        query = select(cls).where(cls.Credit_id == id)
        credits = await db.execute(query)
        (Credit,)= credits.first()
        return Credit
    
    @classmethod
    async def get_all(cls):
        query=select(cls)
        credits =await db.execute(query)
        credits = credits.scalars().all()
        return credits
    
    @classmethod
    async def update(cls,id,**kwargs):
        Credit = await cls.get(id)
        Credit.from_dict(kwargs)

        Credit_dict =Credit.__dict__
        Credit_dict.pop("_sa_instance_state",None)

        query =(
            sqlalchemy_update(cls)
            .where(cls.id == id)
            .values(**Credit_dict)
            .execution_options(synchronize_session=False)
        )

        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise

        return Credit_dict
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