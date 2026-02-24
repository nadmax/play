from pydantic import BaseModel, ConfigDict, HttpUrl, Field


class CompanyBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=255)
    country: str = Field(min_length=2, max_length=100)
    founded_year: int | None = Field(default=None, ge=1800, le=2100)
    website: HttpUrl | None = None
    description: str | None = Field(default=None, max_length=5000)


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, min_length=1, max_length=255)
    country: str | None = Field(default=None, min_length=2, max_length=100)
    founded_year: int | None = Field(default=None, ge=1800, le=2100)
    website: HttpUrl | None = None
    description: str | None = Field(default=None, max_length=5000)


class CompanyResponse(CompanyBase):
    model_config = ConfigDict(from_attributes=True, extra="ignore")

    id: int


class CompanyWithTeams(CompanyResponse):
    model_config = ConfigDict(from_attributes=True, extra="ignore")

    teams: list["TeamResponse"] = []


class TeamBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=255)
    specialty: str = Field(min_length=1, max_length=100)
    size: int | None = Field(default=None, ge=1, le=100000)
    description: str | None = Field(default=None, max_length=5000)
    company_id: int


class TeamCreate(TeamBase):
    pass


class TeamUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, min_length=1, max_length=255)
    specialty: str | None = Field(default=None, min_length=1, max_length=100)
    size: int | None = Field(default=None, ge=1, le=100000)
    description: str | None = Field(default=None, max_length=5000)
    company_id: int | None = None  # ← bug fix


class TeamResponse(TeamBase):
    model_config = ConfigDict(from_attributes=True, extra="ignore")

    id: int

