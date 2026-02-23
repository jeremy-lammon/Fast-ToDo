from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from typing import Annotated
from fastapi import Depends
import os


SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL')
print(SQLALCHEMY_DATABASE_URL)
if SQLALCHEMY_DATABASE_URL is None:
    print("WARNING: No Database URL env variable provided. Running new database from memory.")
    SQLALCHEMY_DATABASE_URL = 'sqlite+aiosqlite:///file:mem_db1?mode=memory&cache=shared&uri=true'

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, pool_recycle=300)

async_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()

DbSession = Annotated[AsyncSession, Depends(get_db)]