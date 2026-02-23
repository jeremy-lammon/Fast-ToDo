from fastapi import APIRouter

from src.tasks.schemas import TaskCreate, TaskRead, TaskUpdate
from src.tasks.service import TaskServiceDep

TaskRouter = APIRouter(prefix="/api/users/{user_id}/tasks", tags=["tasks"])

@TaskRouter.get("/", response_model=list[TaskRead])
async def get_user_tasks(user_id: int, service: TaskServiceDep):
    return await service.get_tasks_by_user(user_id)

@TaskRouter.post("/", response_model=TaskRead, status_code=201)
async def create_task(user_id: int, data: TaskCreate, service: TaskServiceDep):
    return await service.create_task(user_id, data)

@TaskRouter.get("/{task_id}", response_model=TaskRead)
async def get_task(user_id: int, task_id: int, service: TaskServiceDep):
    return await service.get_by_id(task_id)

@TaskRouter.put("/{task_id}", response_model=TaskRead)
async def update_task(user_id: int, task_id: int, data: TaskUpdate, service: TaskServiceDep):
    return await service.update_task(task_id, data)

@TaskRouter.delete("/{task_id}")
async def delete_task(user_id: int, task_id: int, service: TaskServiceDep):
    return await service.delete_task(task_id)