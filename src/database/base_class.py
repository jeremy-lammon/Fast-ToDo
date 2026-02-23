from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass


async def init_db():
    from src.database.db import engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)