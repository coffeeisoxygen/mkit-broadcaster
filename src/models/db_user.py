from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from src.models import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        __name_pos=Integer(), primary_key=True, autoincrement=True
    )
    username: Mapped[str] = mapped_column(
        __name_pos=String(length=100), nullable=False, unique=True
    )
    full_name: Mapped[str] = mapped_column(
        __name_pos=String(length=100), nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        __name_pos=String(length=100), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(__name_pos=Boolean(), default=True)
    is_superuser: Mapped[bool] = mapped_column(__name_pos=Boolean(), default=False)
    created_at: Mapped[datetime] = mapped_column(
        __name_pos=DateTime(timezone=True), default=datetime.now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        __name_pos=DateTime(timezone=True),
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False,
    )
