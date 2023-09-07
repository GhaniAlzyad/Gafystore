from sqlalchemy import Column,String,DateTime,BigInteger
from sqlalchemy import false, true 
from sqlalchemy import delete as sqlalchemy_delete, update as sqlalchemy_update
from sqlalchemy import select
from ...database import base, db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from ..schema.login_schema import LoginSchema
from hashlib import sha256
import os


class User(base):
    __tablename__ = 'users'
    id = Column(BigInteger,primary_key=True,autoincrement=True)
    name = Column(String(255), nullable=False)
    username = Column(String(255),unique=True,nullable=False)
    password = Column(String(255),nullable=False)
    email = Column(String(255),unique=True,nullable=False)
    created_at = Column(DateTime,server_defaul=datetime.utcnow().strftime("%Y-%m-%D %H:%M:%S"))
    
    def __repr__(self):
        return f"<user: ({self.name})"
    
    @classmethod
    async def create(cls,**kwargs):
        user = cls(**kwargs)

        db.add(user)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return user
    
    @classmethod
    async def get(cls, id):
        query = select(cls).where(cls.id == id)
        users = await db.execute(query)
        (user,)= users.first()
        return user
    
    @classmethod
    async def get_all(cls):
        query=select(cls)
        users =await db.execute(query)
        users = users.scalars().all()
        return users
    
    @classmethod
    async def update(cls,id,**kwargs):
        user = await cls.get(id)
        user.from_dict(kwargs)

        user_dict =user.__dict__
        user_dict.pop("_sa_instance_state",None)

        query =(
            sqlalchemy_update(cls)
            .where(cls.id == id)
            .values(**user_dict)
            .execution_options(synchronize_session=False)
        )

        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise

        return user_dict
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
    
    @classmethod
    async def getByUser(cls,username):
        query = select(cls).where(cls.username == username)
        users = await db.execute(query)
        (user,) = users.first()
       
        return user
    
    @classmethod
    async def login(cls,param: LoginSchema):
        user = await cls.getByUser(param.username)
        res = user.to_response()
        print(f"res<{res}>")
        if user is None or not check_password_hash(res.password,param.password):
            return None
        
        return True
    

        
    def to_response(self) -> LoginSchema:
        return LoginSchema(
            username=self.username,
            password=self.password
        )
    
    def from_dict(self, data):
        fields=[
            'name', 'email', 'username', 'password','role_id',
        ]
        for field in fields:
            value = data.get(field)
            if value is not None:
                setattr(self, field, value)