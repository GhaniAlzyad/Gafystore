from sqlalchemy import  Column, Integer, DateTime,String
from sqlalchemy import false, true 
from sqlalchemy import delete as sqlalchemy_delete, update as sqlalchemy_update
from sqlalchemy import select
from ...database import base, db
from datetime import datetime

class Account(base):
    __tablename__ = 'accounts'
    
    account_id = Column(Integer, primary_key=True)
    game_id = Column(Integer)
    items = Column(String(255), nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Account:({self.game_id})"
    
        
    @classmethod
    async def create(cls,**kwargs):
        Account = cls(**kwargs)
        db.add(Account)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return Account
    
    @classmethod
    async def get(cls, id):
        query = select(cls).where(cls.account_id == id)
        accounts = await db.execute(query)
        (Account,)= accounts.first()
        return Account
    
    @classmethod
    async def get_all(cls):
        query=select(cls)
        accounts =await db.execute(query)
        accounts = accounts.scalars().all()
        return accounts
    
    @classmethod
    async def update(cls,id,**kwargs):
        Account = await cls.get(id)
        Account.from_dict(kwargs)

        Account_dict =Account.__dict__
        Account_dict.pop("_sa_instance_state",None)

        query =(
            sqlalchemy_update(cls)
            .where(cls.id == id)
            .values(**Account_dict)
            .execution_options(synchronize_session=False)
        )

        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise

        return Account_dict
    
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
            'username', 'game_id', 'level', 'items','date_created',
        ]
        for field in fields:
            value = data.get(field)
            if value is not None:
                setattr(self, field, value)