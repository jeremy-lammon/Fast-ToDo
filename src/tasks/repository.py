from typing import Annotated

from fastapi import Depends
from sqlalchemy import select

from src.database.db import DbSession
from src.tasks.models import TaskModel

class TaskRepository:
    def __init__(self, db: DbSession) -> None:
        self.db = db
    
    async def create(self, task: TaskModel) -> TaskModel:
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task
    
    async def get_task_by_id(self, task_id: int) -> TaskModel | None:
        result = await self.db.execute(select(TaskModel).where(TaskModel.id == task_id))
        return result.scalar_one_or_none()

    async def get_task_by_user_and_id(self, user_id: int, task_id: int) -> TaskModel | None:
        result = await self.db.execute(
            select(TaskModel).where(TaskModel.id == task_id, TaskModel.user_id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def get_tasks_by_user_id(self, user_id: int) -> list[TaskModel]:
        result = await self.db.execute(select(TaskModel).where(TaskModel.user_id == user_id))
        return list(result.scalars().all())
    
    async def get_all(self) -> list[TaskModel]:
        result = await self.db.execute(select(TaskModel))
        return list(result.scalars().all())
    
    async def update_task(self, user: TaskModel) -> TaskModel | None:
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def delete(self, user: TaskModel) -> None:
        await self.db.delete(user)
        await self.db.commit()

TaskRepo = Annotated[TaskRepository, Depends(TaskRepository)]