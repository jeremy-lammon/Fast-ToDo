from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
import os

from typing import Annotated
from fastapi import Depends

SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite+aiosqlite:///file:mem_db1?mode=memory&cache=shared&uri=true')

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, pool_recycle=300)

async_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()

DbSession = Annotated[AsyncSession, Depends(get_db)]