from pydantic import BaseModel


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
