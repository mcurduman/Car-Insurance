from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from sqlalchemy import Integer, String, ForeignKey, Date
from datetime import date
from typing import Optional
from app.db.base import Base

class InsurancePolicy(Base):
    __tablename__ = "insurance_policy"
    id: Mapped[int] = mapped_column(primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("car.id"), nullable=False)
    provider: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    logged_expiry_at: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
