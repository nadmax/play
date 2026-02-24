from pydantic import BaseModel


class TeamBase(BaseModel):
    name: str
    specialty: str
    size: int | None = None
    description: str | None = None
    company_id: int


class TeamCreate(TeamBase):
    pass


class TeamUpdate(BaseModel):
    name: str | None = None
    specialty: str | None = None
    size: int | None = None
    description: str | None = None
    company_id: int | None = None


class TeamResponse(TeamBase):
    id: int

    model_config = {"from_attributes": True}
