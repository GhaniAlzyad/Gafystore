from sqlalchemy import Column,String,DateTime,BigInteger
from sqlalchemy import delete as sqlalchemy_delete, update as sqlalchemy_update
from sqlalchemy import select, or_
from App.database import base, db
from datetime import datetime
from App.src.schema.auth_schema import AuthSchema
from fastapi import HTTPException, status
from uuid import uuid4


class Admin(base):
    __tablename__ = 'admins'
    id = Column(String,primary_key=True)
    name = Column(String(255), nullable=False)
    adminname = Column(String(255),unique=True,nullable=False)
    password = Column(String(255),nullable=False)
    token = Column(String(255), nullable=True)


    def __repr__(self):
        return f"<admin: ({self.name})"

    @classmethod
    async def create(cls,**kwargs):
        admin = cls(id=str(uuid4()), **kwargs)

        db.add(admin)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return admin

    @classmethod
    async def get_by_id(cls, id):
        admin = await db.execute(select(cls).where(cls.id == id))
        admin = admin.scalar_one_or_none()
        if admin is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="admin not found")

        return admin

    @classmethod
    async def get_all(cls):
        query=select(cls)
        admins =await db.execute(query)
        admins = admins.scalars().all()
        return admins

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
        admins = await db.execute(query)
        (admin,) = admins.first()

        return admin

    @classmethod
    async def get_by_email_or_username(cls, param: str):
        admin = await db.execute(select(cls).where(or_(cls.email == param, cls.username == param)))
        admin = admin.scalar_one_or_none()
        if admin is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="admin not found")

        return admin

    @classmethod
    async def get_by_token(cls, token: str):
        admin = await db.execute(select(cls).where(cls.token == token))
        admin = admin.scalar_one_or_none()
        if admin is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

        return admin

    @staticmethod
    async def commit():
        try:
            await db.commit()
        except:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
