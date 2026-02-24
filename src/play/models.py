"""
SQLAlchemy ORM models for the play application.

This module defines the database models representing companies and their teams.
Each model maps to a database table and defines relationships between entities.
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy import orm
from play import database


class Company(database.Base):
    """
    Represents a company entity.

    A company can own multiple teams. This model stores general
    information about a company such as its name, country, and website.

    Attributes:
        id (int): Primary key identifier of the company.
        name (str): Unique name of the company.
        country (str): Country where the company is based.
        founded_year (int | None): Year the company was founded.
        website (str | None): Official website URL of the company.
        description (str | None): Optional textual description of the company.
        teams (list[Team]): List of teams associated with the company.
            Deleting a company will also delete its associated teams.
    """

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
    """
    Represents a team within a company.

    Each team belongs to exactly one company and stores information
    about its specialization and size.

    Attributes:
        id (int): Primary key identifier of the team.
        name (str): Name of the team.
        specialty (str): Main area of expertise of the team.
        size (int | None): Number of members in the team.
        description (str | None): Optional textual description of the team.
        company_id (int): Foreign key referencing the owning company.
        company (Company): The company to which this team belongs.
    """

    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    specialty = Column(String(100), nullable=False)
    size = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    company = orm.relationship("Company", back_populates="teams")
