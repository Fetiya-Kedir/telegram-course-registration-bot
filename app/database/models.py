from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Registration(Base):
    __tablename__ = "registrations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    reference_code: Mapped[str | None] = mapped_column(String(50), nullable=True, unique=True)

    telegram_user_id: Mapped[int] = mapped_column(Integer, index=True)
    telegram_username: Mapped[str | None] = mapped_column(String(100), nullable=True)
    full_name: Mapped[str] = mapped_column(String(200))
    department: Mapped[str] = mapped_column(String(200))
    phone: Mapped[str] = mapped_column(String(30))
    language: Mapped[str] = mapped_column(String(10))
    class_id: Mapped[str] = mapped_column(String(20))
    class_name: Mapped[str] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(String(50), default="new")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)