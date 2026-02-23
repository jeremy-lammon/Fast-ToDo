from fastapi import APIRouter

from src.users.schemas import UserCreate, UserRead, UserUpdate
from src.users.service import UserServiceDep

UserRouter = APIRouter(prefix="/api/users", tags=["users"])

@UserRouter.post("/", response_model=UserRead, status_code=201)
async def create_user(user: UserCreate, user_service: UserServiceDep):
    return await user_service.create_user(user)

@UserRouter.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, user_service: UserServiceDep):
    return await user_service.get_by_id(user_id)

@UserRouter.put("/{user_id}", response_model=UserRead)
async def update_user(user_id: int, user: UserUpdate, user_service: UserServiceDep):
    return await user_service.update_user(user_id, user)

@UserRouter.delete("/{user_id}")
async def delete_user(user_id: int, user_service: UserServiceDep):
    return await user_service.delete_user(user_id)