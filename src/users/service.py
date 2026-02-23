from typing import Annotated

from fastapi import Depends, HTTPException, status

from src.users.models import UserModel
from src.users.repository import UserRepo
from src.users.schemas import UserCreate, UserRead, UserUpdate

from src.exceptions import NotFoundError, ConflictError

class UserService:
    def __init__(self, repo: UserRepo) -> None:
        self.repo = repo
    
    async def _get_or_404(self, user_id: int) -> UserModel:
        user = await self.repo.get_user_by_id(user_id)
        if user is None:
            raise NotFoundError(resource="User", resource_id=user_id)
        return user

    async def get_by_id(self, user_id: int) -> UserRead:
        return UserRead.model_validate(await self._get_or_404(user_id))
    
    async def get_all(self) -> list[UserRead]:
        users = await self.repo.get_all()
        return [UserRead.model_validate(u) for u in users]
    
    async def create_user(self, data: UserCreate) -> UserRead:
        existing = await self.repo.get_user_by_username(data.username)
        if existing:
            raise ConflictError(message="Username already taken", field="username")
        user = await self.repo.create(UserModel(username=data.username))
        return UserRead.model_validate(user)
    
    async def update_user(self, user_id: int, data: UserUpdate) -> UserRead:
        user = await self._get_or_404(user_id)
        if data.username is not None:
            user.username = data.username
        updated = await self.repo.update_user(user)
        return UserRead.model_validate(updated)
    
    async def delete_user(self, user_id: int) -> None:
        await self.repo.delete(await self._get_or_404(user_id))

UserServiceDep = Annotated[UserService, Depends(UserService)]