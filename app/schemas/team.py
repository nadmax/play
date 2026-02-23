from pydantic import BaseModel
from typing import Optional


class TeamBase(BaseModel):
    name: str
    specialty: str
    size: Optional[int] = None
    description: Optional[str] = None
    company_id: int


class TeamCreate(TeamBase):
    pass


class TeamUpdate(BaseModel):
    name: Optional[str] = None
    specialty: Optional[str] = None
    size: Optional[int] = None
    description: Optional[str] = None
    company_id: Optional[int] = None


class TeamResponse(TeamBase):
    id: int

    model_config = {"from_attributes": True}
