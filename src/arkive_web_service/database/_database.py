from __future__ import annotations
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncEngine,
    AsyncSession,
)
from arkive_web_service.settings import settings
import contextlib
from typing import Optional


class Database:
    def __init__(self: Database, url: str, **engine_kwargs):
        self.__engine: Optional[AsyncEngine] = create_async_engine(url, **engine_kwargs)
        self.__sesssion_maker: Optional[async_sessionmaker[AsyncSession]] = (
            async_sessionmaker(bind=self.__engine)
        )

    @contextlib.asynccontextmanager
    async def connect(self: Database):
        if self.__engine is None:
            raise Exception("Database is not initialized")

        async with self.__engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self: Database):
        if self.__sesssion_maker is None:
            raise Exception("Database is not initialized")

        session = self.__sesssion_maker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    @contextlib.asynccontextmanager
    async def close(self: Database):
        if self.__engine is None:
            raise Exception("Database is not initialized")
        await self.__engine.dispose()

        self.__engine = None
        self.__sesssion_maker = None
        yield


db = Database(settings.DATABASE_URL)
