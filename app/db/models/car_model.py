from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Car(Base):
    __tablename__ = "car"
    id = Column(Integer, primary_key=True)
    vin = Column(String, nullable=False, unique=True)
    make = Column(String, nullable=True)
    model = Column(String, nullable=True)
    year_of_manufacture = Column(Integer)
    owner_id = Column(Integer, ForeignKey("owner.id"), nullable=False)
