from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from sqlalchemy import Integer, ForeignKey, Date, Text, Numeric, DateTime, func
from datetime import date, datetime
from app.db.base import Base

class Claim(Base):
    __tablename__ = "claim"
    id: Mapped[int] = mapped_column(primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("car.id"), nullable=False)
    claim_date: Mapped[date] = mapped_column(Date, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
