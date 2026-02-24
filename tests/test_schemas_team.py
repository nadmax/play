import pytest
from pydantic import ValidationError

from app.schemas.team import TeamCreate, TeamUpdate, TeamResponse


def test_team_create_valid():
    team = TeamCreate(name="EPD Group No. 3", specialty="Development", company_id=1)
    assert team.name == "EPD Group No. 3"
    assert team.specialty == "Development"
    assert team.company_id == 1
    assert team.size is None
    assert team.description is None


def test_team_create_missing_required_fields():
    with pytest.raises(ValidationError):
        TeamCreate(name="EPD Group No. 3")


def test_team_create_all_fields():
    team = TeamCreate(
        name="Soulsborne Team",
        specialty="Development",
        size=300,
        description="Core team behind Dark Souls and Elden Ring.",
        company_id=2,
    )
    assert team.size == 300
    assert team.description == "Core team behind Dark Souls and Elden Ring."


def test_team_update_all_optional():
    update = TeamUpdate()
    assert update.name is None
    assert update.specialty is None
    assert update.company_id is None


def test_team_update_partial():
    update = TeamUpdate(name="Updated Team", size=150)
    assert update.name == "Updated Team"
    assert update.size == 150
    assert update.specialty is None


def test_team_response_from_attributes():
    response = TeamResponse.model_validate(
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
