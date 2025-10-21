from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from sqlalchemy import Integer, String, ForeignKey
from app.db.base import Base
from typing import Optional

class Car(Base):
    __tablename__ = "car"
    id: Mapped[int] = mapped_column(primary_key=True)
    vin: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    make: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    model: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    year_of_manufacture: Mapped[Optional[int]] = mapped_column(Integer)
    owner_id: Mapped[int] = mapped_column(ForeignKey("owner.id"), nullable=False)
