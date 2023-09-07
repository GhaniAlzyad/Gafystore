from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from .config import config

base = declarative_base()


class AsyncDatabaseSession():
    def __init__(self):
        self._session = None
        self. engine = None

    def __getattr__(self, name):
        return getattr(self._session, name)
    
    def init(self):
        self._engine = create_async_engine(
            config.DB_CONFIG,
            future=True,
            echo=True,
            )
        self._session = sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )()

    async def create_all(self):
        async with self._engine.begin() as corn:
            await corn.run_sync(base.metadata.create_all)

db=AsyncDatabaseSession()