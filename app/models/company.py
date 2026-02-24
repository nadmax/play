from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    country = Column(String(100), nullable=False)
    founded_year = Column(Integer, nullable=True)
    website = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)

    teams = relationship("Team", back_populates="company", cascade="all, delete-orphan")
