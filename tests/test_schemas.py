import pytest
from pydantic import ValidationError

from play import schemas


def test_company_create_valid():
    company = schemas.CompanyCreate(name="Nintendo", country="Japan", founded_year=1889)
    assert company.name == "Nintendo"
    assert company.country == "Japan"
    assert company.founded_year == 1889
    assert company.website is None
    assert company.description is None


def test_company_create_missing_required_fields():
    with pytest.raises(ValidationError):
        schemas.CompanyCreate(name="Nintendo")


def test_company_create_all_fields():
    company = schemas.CompanyCreate(
        name="Ubisoft",
        country="France",
        founded_year=1986,
        website="https://www.ubisoft.com",
        description="French video game publisher.",
    )
    assert company.website == "https://www.ubisoft.com"
    assert company.description == "French video game publisher."


def test_company_update_all_optional():
    update = schemas.CompanyUpdate()
    assert update.name is None
    assert update.country is None
    assert update.founded_year is None


def test_company_update_partial():
    update = schemas.CompanyUpdate(name="Ubisoft Updated")
    assert update.name == "Ubisoft Updated"
    assert update.country is None


def test_company_response_from_attributes():
    response = schemas.CompanyResponse.model_validate(
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
    company = schemas.CompanyWithTeams.model_validate(
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


def test_team_create_valid():
    team = schemas.TeamCreate(
        name="EPD Group No. 3", specialty="Development", company_id=1
    )
    assert team.name == "EPD Group No. 3"
    assert team.specialty == "Development"
    assert team.company_id == 1
    assert team.size is None
    assert team.description is None


def test_team_create_missing_required_fields():
    with pytest.raises(ValidationError):
        schemas.TeamCreate(name="EPD Group No. 3")


def test_team_create_all_fields():
    team = schemas.TeamCreate(
        name="Soulsborne Team",
        specialty="Development",
        size=300,
        description="Core team behind Dark Souls and Elden Ring.",
        company_id=2,
    )
    assert team.size == 300
    assert team.description == "Core team behind Dark Souls and Elden Ring."


def test_team_update_all_optional():
    update = schemas.TeamUpdate(company_id=1)
    assert update.name is None
    assert update.specialty is None
    assert update.company_id == 1


def test_team_update_partial():
    update = schemas.TeamUpdate(name="Updated Team", size=150, company_id=1)
    assert update.name == "Updated Team"
    assert update.size == 150
    assert update.specialty is None


def test_team_response_from_attributes():
    response = schemas.TeamResponse.model_validate(
        {
            "id": 1,
            "name": "Steam Platform Team",
            "specialty": "Platform",
            "size": 200,
            "description": None,
            "company_id": 3,
        }
    )
    assert response.id == 1
    assert response.company_id == 3
