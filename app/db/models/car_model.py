from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from sqlalchemy import Integer, String, ForeignKey

Base = declarative_base()

class Car(Base):
    __tablename__ = "car"
    id: Mapped[int] = mapped_column(primary_key=True)
    vin: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    make: Mapped[str | None] = mapped_column(String, nullable=True)
    model: Mapped[str | None] = mapped_column(String, nullable=True)
    year_of_manufacture: Mapped[int | None] = mapped_column(Integer)
    owner_id: Mapped[int] = mapped_column(ForeignKey("owner.id"), nullable=False)
