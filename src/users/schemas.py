from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    username: str

class UserCreate(BaseModel):
    pass

class UserUpdate(BaseModel):
    username: str | None = None

class UserRead(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)