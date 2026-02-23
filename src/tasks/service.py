from typing import Annotated

from fastapi import Depends, HTTPException, status

from src.tasks.models import TaskModel
from src.tasks.repository import TaskRepo
from src.tasks.schemas import TaskCreate, TaskRead, TaskUpdate

# TODO: Proper custom global Error classes to abstract away FastApi's exceptions.

class TaskService:
    def __init__(self, repo: TaskRepo) -> None:
        self.repo = repo
    
    async def _get_or_404(self, task_id: int) -> TaskModel:
        task = await self.repo.get_task_by_id(task_id)
        if task is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        return task

    async def get_by_id(self, task_id: int) -> TaskRead:
        return TaskRead.model_validate(await self._get_or_404(task_id))
    
    async def get_tasks_by_user(self, user_id: int) -> list[TaskRead]:
        tasks = await self.repo.get_tasks_by_user_id(user_id)
        return [TaskRead.model_validate(t) for t in tasks]
    
    async def create_task(self, user_id: int, data: TaskCreate) -> TaskRead:
        task = await self.repo.create(TaskModel(title=data.title, description=data.description, user_id=data.user_id))
        return TaskRead.model_validate(task)
    
    async def update_task(self, task_id: int, data: TaskUpdate) -> TaskRead:
        task = await self._get_or_404(task_id)
        if data.title is not None:
            task.title = data.title
        if data.description is not None:
            task.description = data.description
        updated = await self.repo.update_task(task)
        return TaskRead.model_validate(updated)
    
    async def delete_task(self, task_id: int) -> None:
        await self.repo.delete(await self._get_or_404(task_id))

TaskServiceDep = Annotated[TaskService, Depends(TaskService)]