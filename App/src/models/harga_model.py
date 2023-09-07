from sqlalchemy import  Column, Integer
from sqlalchemy import false, true 
from sqlalchemy import delete as sqlalchemy_delete, update as sqlalchemy_update
from sqlalchemy import select
from ...database import base, db
from datetime import datetime

class Harga(base):
    __tablename__ = 'harga'
    
    id_jumlah = Column(Integer, primary_key=True)
    jumlah_credit_game = Column(Integer)
    harga = Column(Integer)

    def __repr__(self):
        return f"<Harga:({self.id_jumlah})"
    
        
    @classmethod
    async def create(cls,**kwargs):
        Harga = cls(**kwargs)
        db.add(Harga)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return Harga
    
    @classmethod
    async def get(cls, id):
        query = select(cls).where(cls.Harga_id == id)
        harga = await db.execute(query)
        (Harga,)= harga.first()
        return Harga
    
    @classmethod
    async def get_all(cls):
        query=select(cls)
        harga =await db.execute(query)
        harga = harga.scalars().all()
        return harga
    
    @classmethod
    async def update(cls,id,**kwargs):
        Harga = await cls.get(id)
        Harga.from_dict(kwargs)

        Harga_dict =Harga.__dict__
        Harga_dict.pop("_sa_instance_state",None)

        query =(
            sqlalchemy_update(cls)
            .where(cls.id == id)
            .values(**Harga_dict)
            .execution_options(synchronize_session=False)
        )

        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise

        return Harga_dict
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
            'jumlah_credit_game', 'harga',
        ]
        for field in fields:
            value = data.get(field)
            if value is not None:
                setattr(self, field, value)