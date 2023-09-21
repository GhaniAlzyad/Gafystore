from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import false, true
from sqlalchemy import delete as sqlalchemy_delete, update as sqlalchemy_update
from sqlalchemy import select
from ...database import base, db
from datetime import datetime
from fastapi import HTTPException, status


class Game(base):
    __tablename__ = 'Games'

    game_id = Column(Integer, primary_key=True,autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    genre = Column(String(255),nullable=False)
    release_date = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<Game:({self.title})"


    @classmethod
    async def create(cls,**kwargs):
        Game = cls(**kwargs)
        db.add(Game)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return Game

    @classmethod
    async def get(cls, id):
        query = await db.execute(select(cls).where(cls.game_id == id))
        game = query.scalar_one_or_none()
        if game is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")

        return Game

    @classmethod
    async def get_all(cls):
        query=select(cls)
        Games =await db.execute(query)
        Games = Games.scalars().all()
        return Games

    @classmethod
    async def update(cls,id,**kwargs):
        Game = await cls.get(id)
        Game.from_dict(kwargs)

        Game_dict =Game.__dict__
        Game_dict.pop("_sa_instance_state",None)

        query =(
            sqlalchemy_update(cls)
            .where(cls.id == id)
            .values(**Game_dict)
            .execution_options(synchronize_session=False)
        )

        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise

        return Game_dict
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
    async def get_by_name_or_description(cls, param):
        query = select(cls).where(
            (cls.title.like(f"%{param}%")) | (cls.description.like(f"%{param}%"))
        )
        Games = await db.execute(query)
        Games = Games.scalars().all()
        return Games

    def from_dict(self, data):
        fields=[
            'tittle', 'description', 'genre', 'release_date',
        ]
        for field in fields:
            value = data.get(field)
            if value is not None:
                setattr(self, field, value)