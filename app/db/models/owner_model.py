from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from sqlalchemy import Integer, String

Base = declarative_base()

class Owner(Base):
    __tablename__ = "owner"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str | None] = mapped_column(String, nullable=True)
