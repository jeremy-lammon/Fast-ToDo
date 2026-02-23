from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.base_class import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.tasks.models import TaskModel

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)

    tasks: Mapped[list["TaskModel"]] = relationship(back_populates="user")

