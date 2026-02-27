from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum
from db.base import Base
from sqlalchemy.orm import Mapped, mapped_column

class UserRole(str, Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    username: Mapped[str] = mapped_column()
    hashed_password: Mapped[str] = mapped_column()
    role: Mapped[UserRole] = mapped_column(SQLAlchemyEnum(UserRole), default=UserRole.USER)
    is_active: Mapped[bool] = mapped_column(default=True)