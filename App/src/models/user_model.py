from sqlalchemy import Column,String,DateTime,BigInteger
from sqlalchemy import delete as sqlalchemy_delete, update as sqlalchemy_update
from sqlalchemy import select, or_
from App.database import base, db
from datetime import datetime
from App.src.schema.auth_schema import AuthSchema
from fastapi import HTTPException, status
from uuid import uuid4


class User(base):
    __tablename__ = 'users'
    id = Column(String,primary_key=True)
    name = Column(String(255), nullable=False)
    username = Column(String(255),unique=True,nullable=False)
    password = Column(String(255),nullable=False)
    email = Column(String(255),unique=True,nullable=False)
    token = Column(String(255), nullable=True)
    expired_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime,server_defaul=datetime.utcnow().strftime("%Y-%m-%D %H:%M:%S"))

    def __repr__(self):
        return f"<user: ({self.name})"

    @classmethod
    async def create(cls,**kwargs):
        user = cls(id=str(uuid4()), **kwargs)

        db.add(user)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return user

    @classmethod
    async def get_by_id(cls, id):
        user = await db.execute(select(cls).where(cls.id == id))
        user = user.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user

    @classmethod
    async def get_all(cls):
        query=select(cls)
        users =await db.execute(query)
        users = users.scalars().all()
        return users

    @classmethod
    async def update(cls,obj: dict):
        await db.execute(sqlalchemy_update(cls).where(cls.id == obj['id']).values(obj))

        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

        return obj

    @classmethod
    async def delete(cls, id):
        query = sqlalchemy_delete(cls).where(cls.id == id)
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
        return True

    @classmethod
    async def getByUser(cls,username):
        query = select(cls).where(cls.username == username)
        users = await db.execute(query)
        (user,) = users.first()

        return user

    @classmethod
    async def get_by_email_or_username(cls, param: str):
        user = await db.execute(select(cls).where(or_(cls.email == param, cls.username == param)))
        user = user.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user

    @classmethod
    async def get_by_token(cls, token: str):
        user = await db.execute(select(cls).where(cls.token == token))
        user = user.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

        return user

    @staticmethod
    async def commit():
        try:
            await db.commit()
        except:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
