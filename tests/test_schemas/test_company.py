import pytest
from pydantic import ValidationError

from app.schemas.company import (
    CompanyCreate,
    CompanyUpdate,
    CompanyResponse,
    CompanyWithTeams,
)


def test_company_create_valid():
    company = CompanyCreate(name="Nintendo", country="Japan", founded_year=1889)
    assert company.name == "Nintendo"
    assert company.country == "Japan"
    assert company.founded_year == 1889
    assert company.website is None
    assert company.description is None


def test_company_create_missing_required_fields():
    with pytest.raises(ValidationError):
        CompanyCreate(name="Nintendo")


def test_company_create_all_fields():
    company = CompanyCreate(
        name="Ubisoft",
        country="France",
        founded_year=1986,
        website="https://www.ubisoft.com",
        description="French video game publisher.",
    )
    assert company.website == "https://www.ubisoft.com"
    assert company.description == "French video game publisher."


def test_company_update_all_optional():
    update = CompanyUpdate()
    assert update.name is None
    assert update.country is None
    assert update.founded_year is None


def test_company_update_partial():
    update = CompanyUpdate(name="Ubisoft Updated")
    assert update.name == "Ubisoft Updated"
    assert update.country is None


def test_company_response_from_attributes():
    response = CompanyResponse.model_validate(
        {
            "id": 1,
            "name": "Valve",
            "country": "USA",
            "founded_year": 1996,
            "website": None,
            "description": None,
        }
    )
    assert response.id == 1
    assert response.name == "Valve"


def test_company_with_teams_empty_teams():
    company = CompanyWithTeams.model_validate(
        {
            "id": 1,
            "name": "FromSoftware",
            "country": "Japan",
            "founded_year": 1986,
            "website": None,
            "description": None,
            "teams": [],
        }
    )
    assert company.teams == []
