from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.base_class import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.users.models import UserModel

class TaskModel(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str | None] = mapped_column(default=None)
    completed: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["UserModel"] = relationship(back_populates="tasks")