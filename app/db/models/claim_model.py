from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from sqlalchemy import Integer, ForeignKey, Date, Text, Numeric, DateTime, func

Base = declarative_base()

class Claim(Base):
    __tablename__ = "claim"
    id: Mapped[int] = mapped_column(primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("car.id"), nullable=False)
    claim_date: Mapped[Date] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=func.now())
