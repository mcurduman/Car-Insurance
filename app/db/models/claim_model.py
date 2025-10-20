from sqlalchemy import Column, Integer, ForeignKey, Date, Text, Numeric, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Claim(Base):
    __tablename__ = "claim"
    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey("car.id"), nullable=False)
    claim_date = Column(Date, nullable=False)
    description = Column(Text, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
