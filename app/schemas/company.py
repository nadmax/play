from pydantic import BaseModel
from typing import Optional, List
from .team import TeamResponse


class CompanyBase(BaseModel):
    name: str
    country: str
    founded_year: Optional[int] = None
    website: Optional[str] = None
    description: Optional[str] = None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None
    founded_year: Optional[int] = None
    website: Optional[str] = None
    description: Optional[str] = None


class CompanyResponse(CompanyBase):
    id: int

    model_config = {"from_attributes": True}


class CompanyWithTeams(CompanyResponse):
    teams: List["TeamResponse"] = []

    model_config = {"from_attributes": True}


CompanyWithTeams.model_rebuild()
