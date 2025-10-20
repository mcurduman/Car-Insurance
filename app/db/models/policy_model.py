from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from sqlalchemy import Integer, String, ForeignKey, Date

Base = declarative_base()

class InsurancePolicy(Base):
    __tablename__ = "insurance_policy"
    id: Mapped[int] = mapped_column(primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("car.id"), nullable=False)
    provider: Mapped[str | None] = mapped_column(String, nullable=True)
    start_date: Mapped[Date] = mapped_column(nullable=False)
    end_date: Mapped[Date] = mapped_column(nullable=False)
    logged_expiry_at: Mapped[Date | None] = mapped_column(nullable=True)
    
