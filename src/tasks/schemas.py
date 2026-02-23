from pydantic import BaseModel, ConfigDict

class TaskBase(BaseModel):
    title: str
    description: str | None = None


class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None

class TaskRead(TaskBase):
    id: int
    completed: bool
    user_id: int
    
    model_config = ConfigDict(from_attributes=True)