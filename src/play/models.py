from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy import orm
from play import database


class Company(database.Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    country = Column(String(100), nullable=False)
    founded_year = Column(Integer, nullable=True)
    website = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)

    teams = orm.relationship(
        "Team", back_populates="company", cascade="all, delete-orphan"
    )


class Team(database.Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    specialty = Column(String(100), nullable=False)
    size = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    company = orm.relationship("Company", back_populates="teams")
