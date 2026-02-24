"""
Pydantic schemas for the play application.

This module defines request and response data models used for
validation and serialization of Company and Team entities.

Schemas are organized by purpose:
- Base: shared attributes
- Create: schema used for creation payloads
- Update: schema used for partial updates
- Response: schema used for API responses
"""

from pydantic import BaseModel, ConfigDict, HttpUrl, Field


class CompanyBase(BaseModel):
    """
    Base schema for Company data.

    Defines shared attributes and validation rules for company-related
    operations.

    Attributes:
        name (str): Name of the company.
        country (str): Country where the company is based.
        founded_year (int | None): Year the company was founded
            (between 1800 and 2100).
        website (HttpUrl | None): Official website URL.
        description (str | None): Optional description of the company
            (maximum 5000 characters).
    """

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=255)
    country: str = Field(min_length=2, max_length=100)
    founded_year: int | None = Field(default=None, ge=1800, le=2100)
    website: HttpUrl | None = None
    description: str | None = Field(default=None, max_length=5000)


class CompanyCreate(CompanyBase):
    """
    Schema used for creating a new Company.

    Inherits all required fields from CompanyBase.
    """

    pass


class CompanyUpdate(BaseModel):
    """
    Schema used for updating an existing Company.

    All fields are optional to allow partial updates.
    Extra fields are forbidden.
    """

    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, min_length=1, max_length=255)
    country: str | None = Field(default=None, min_length=2, max_length=100)
    founded_year: int | None = Field(default=None, ge=1800, le=2100)
    website: HttpUrl | None = None
    description: str | None = Field(default=None, max_length=5000)


class CompanyResponse(CompanyBase):
    """
    Schema returned in API responses for a Company.

    Attributes:
        id (int): Unique identifier of the company.
    """

    model_config = ConfigDict(from_attributes=True, extra="ignore")

    id: int


class CompanyWithTeams(CompanyResponse):
    """
    Extended company response including related teams.

    Attributes:
        teams (list[TeamResponse]): List of teams associated
            with the company.
    """

    model_config = ConfigDict(from_attributes=True, extra="ignore")

    teams: list["TeamResponse"] = []


class TeamBase(BaseModel):
    """
    Base schema for Team data.

    Defines shared attributes and validation rules for team-related
    operations.

    Attributes:
        name (str): Name of the team.
        specialty (str): Area of expertise of the team.
        size (int | None): Number of team members (between 1 and 100000).
        description (str | None): Optional description of the team
            (maximum 5000 characters).
        company_id (int): Identifier of the associated company.
    """

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=255)
    specialty: str = Field(min_length=1, max_length=100)
    size: int | None = Field(default=None, ge=1, le=100000)
    description: str | None = Field(default=None, max_length=5000)
    company_id: int


class TeamCreate(TeamBase):
    """
    Schema used for creating a new Team.

    Inherits all required fields from TeamBase.
    """

    pass


class TeamUpdate(BaseModel):
    """
    Schema used for updating an existing Team.

    All fields are optional to allow partial updates.
    """

    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, min_length=1, max_length=255)
    specialty: str | None = Field(default=None, min_length=1, max_length=100)
    size: int | None = Field(default=None, ge=1, le=100000)
    description: str | None = Field(default=None, max_length=5000)
    company_id: int | None = None  # ← bug fix


class TeamResponse(TeamBase):
    """
    Schema returned in API responses for a Team.

    Attributes:
        id (int): Unique identifier of the team.
    """

    model_config = ConfigDict(from_attributes=True, extra="ignore")

    id: int
