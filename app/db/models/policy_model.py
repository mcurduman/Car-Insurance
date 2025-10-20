from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class InsurancePolicy(Base):
    __tablename__ = "insurance_policy"
    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey("car.id"), nullable=False)
    provider = Column(String, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    
