from typing import Annotated

from fastapi import Depends
from sqlalchemy import select

from src.database.db import DbSession
from src.users.models import UserModel

class UserRepository:
    def __init__(self, db: DbSession) -> None:
        self.db = db
    
    async def create(self, user:UserModel) -> UserModel:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def get_user_by_id(self, user_id: int) -> UserModel | None:
        result = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
        return result.scalar_one_or_none()
    
    async def get_user_by_username(self, username: str) -> UserModel  | None:
        result = await self.db.execute(select(UserModel).where(UserModel.username == username))
        return result.scalar_one_or_none()
    
    async def get_all(self) -> list[UserModel]:
        result = await self.db.execute(select(UserModel))
        return list(result.scalars().all())
    
    async def update_user(self, user: UserModel) -> UserModel | None:
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def delete(self, user: UserModel) -> UserModel | None:
        await self.db.delete(user)
        await self.db.commit()

UserRepo = Annotated[UserRepository, Depends(UserRepository)]