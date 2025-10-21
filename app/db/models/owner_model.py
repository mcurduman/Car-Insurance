from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from app.db.base import Base
from typing import Optional

class Owner(Base):
    __tablename__ = "owner"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    cars = relationship("Car", cascade="all, delete-orphan", back_populates="owner")
