from pydantic import BaseModel
from .team import TeamResponse


class CompanyBase(BaseModel):
    name: str
    country: str
    founded_year: int | None = None
    website: str | None = None
    description: str | None = None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: str | None = None
    country: str | None = None
    founded_year: int | None = None
    website: str | None = None
    description: str | None = None


class CompanyResponse(CompanyBase):
    id: int

    model_config = {"from_attributes": True}


class CompanyWithTeams(CompanyResponse):
    teams: list["TeamResponse"] = []

    model_config = {"from_attributes": True}
