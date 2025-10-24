from sqlalchemy.orm import Mapped, mapped_column, declarative_base, relationship
from sqlalchemy import Integer, String, ForeignKey
from app.db.base import Base
from typing import Optional
from app.db.models.claim_model import Claim
from app.db.models.owner_model import Owner

class Car(Base):
    __tablename__ = "car"
    id: Mapped[int] = mapped_column(primary_key=True)
    vin: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    make: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    model: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    year_of_manufacture: Mapped[Optional[int]] = mapped_column(Integer)
    owner_id: Mapped[int] = mapped_column(ForeignKey("owner.id"), nullable=False)

    policies = relationship("InsurancePolicy", cascade="all, delete-orphan", back_populates="car")
    claims = relationship("Claim", cascade="all, delete-orphan", back_populates="car")
    owner = relationship("Owner", back_populates="cars")
