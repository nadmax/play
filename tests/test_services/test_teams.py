import pytest
from fastapi import HTTPException

from play import models, schemas
from play.services import teams


def make_company(db, name="Nintendo"):
    company = models.Company(name=name, country="Japan")
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


def make_team(db, company_id, name="Mario Team", specialty="Development"):
    team = models.Team(name=name, specialty=specialty, company_id=company_id)
    db.add(team)
    db.commit()
    db.refresh(team)
    return team


def test_list_teams_empty(db):
    assert teams.list_teams(db) == []


def test_list_teams_returns_all(db):
    company = make_company(db)
    make_team(db, company.id, name="Team A")
    make_team(db, company.id, name="Team B")
    result = teams.list_teams(db)
    assert len(result) == 2


def test_list_teams_skip_and_limit(db):
    company = make_company(db)
    for name in ["A", "B", "C"]:
        make_team(db, company.id, name=name)
    result = teams.list_teams(db, skip=1, limit=1)
    assert len(result) == 1
    assert result[0].name == "B"


def test_get_team_returns_team(db):
    company = make_company(db)
    team = make_team(db, company.id)
    result = teams.get_team(db, team.id)
    assert result.id == team.id
    assert result.name == "Mario Team"


def test_get_team_not_found(db):
    with pytest.raises(HTTPException) as exc:
        teams.get_team(db, 999)
    assert exc.value.status_code == 404
    assert exc.value.detail == "Team not found"


def test_create_team_success(db):
    company = make_company(db)
    payload = schemas.TeamCreate(
        name="Zelda Team", specialty="Development", company_id=company.id
    )
    result = teams.create_team(db, payload)
    assert result.id is not None
    assert result.company_id == company.id


def test_create_team_company_not_found(db):
    payload = schemas.TeamCreate(
        name="Ghost Team", specialty="Development", company_id=999
    )
    with pytest.raises(HTTPException) as exc:
        teams.create_team(db, payload)
    assert exc.value.status_code == 404
    assert exc.value.detail == "Company not found"


def test_update_team_success(db):
    company = make_company(db)
    team = make_team(db, company.id)
    payload = schemas.TeamUpdate(name="DK Team", company_id=company.id)
    result = teams.update_team(db, team.id, payload)
    assert result.name == "DK Team"
    assert result.company_id == company.id


def test_update_team_change_company(db):
    company_a = make_company(db, name="Nintendo")
    company_b = make_company(db, name="Sega")
    team = make_team(db, company_a.id)
    payload = schemas.TeamUpdate(company_id=company_b.id)
    result = teams.update_team(db, team.id, payload)
    assert result.company_id == company_b.id


def test_update_team_company_not_found(db):
    company = make_company(db)
    team = make_team(db, company.id)
    payload = schemas.TeamUpdate(company_id=999)
    with pytest.raises(HTTPException) as exc:
        teams.update_team(db, team.id, payload)
    assert exc.value.status_code == 404
    assert exc.value.detail == "Company not found"


def test_update_team_not_found(db):
    payload = schemas.TeamUpdate(name="Ghost", company_id=999)
    with pytest.raises(HTTPException) as exc:
        teams.update_team(db, 999, payload)
    assert exc.value.status_code == 404


def test_delete_team_success(db):
    company = make_company(db)
    team = make_team(db, company.id)
    teams.delete_team(db, team.id)
    with pytest.raises(HTTPException):
        teams.get_team(db, team.id)


def test_delete_team_not_found(db):
    with pytest.raises(HTTPException) as exc:
        teams.delete_team(db, 999)
    assert exc.value.status_code == 404
