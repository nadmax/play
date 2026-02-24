import pytest
from app.models import Company, Team


def make_company(db, name="Nintendo", country="Japan"):
    company = Company(name=name, country=country)
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


def make_team(db, company_id, name="Mario Team", specialty="Development"):
    team = Team(name=name, specialty=specialty, company_id=company_id)
    db.add(team)
    db.commit()
    db.refresh(team)
    return team


@pytest.fixture
def company(db):
    company = make_company(db)
    db.expunge(company)
    return company


def test_list_teams_empty(client):
    response = client.get("/teams/")
    assert response.status_code == 200
    assert response.json() == []


def test_list_teams(client, db, company):
    make_team(db, company.id, name="EPD Group No. 1")
    make_team(db, company.id, name="EPD Group No. 3")
    response = client.get("/teams/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_team(client, db, company):
    team = make_team(db, company.id, name="NST", specialty="Studio")
    response = client.get(f"/teams/{team.id}")
    assert response.status_code == 200
    assert response.json()["name"] == "NST"


def test_get_team_not_found(client):
    response = client.get("/teams/9999")
    assert response.status_code == 404


def test_create_team(client, company):
    payload = {
        "name": "EPD Group No. 3",
        "specialty": "Development",
        "company_id": company.id,
    }
    response = client.post("/teams/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "EPD Group No. 3"
    assert data["company_id"] == company.id


def test_create_team_company_not_found(client):
    payload = {"name": "Ghost Team", "specialty": "Development", "company_id": 9999}
    response = client.post("/teams/", json=payload)
    assert response.status_code == 404


def test_create_team_missing_field(client, company):
    response = client.post(
        "/teams/", json={"name": "EPD Group No. 3", "company_id": company.id}
    )
    assert response.status_code == 422


def test_update_team(client, db, company):
    team = make_team(db, company.id, name="NST", specialty="Studio")
    response = client.patch(f"/teams/{team.id}", json={"size": 80})
    assert response.status_code == 200
    assert response.json()["size"] == 80


def test_update_team_company_not_found(client, db, company):
    team = make_team(db, company.id, name="NST", specialty="Studio")
    response = client.patch(f"/teams/{team.id}", json={"company_id": 9999})
    assert response.status_code == 404


def test_update_team_not_found(client):
    response = client.patch("/teams/9999", json={"name": "Ghost"})
    assert response.status_code == 404


def test_delete_team(client, db, company):
    team = make_team(db, company.id, name="NST", specialty="Studio")
    response = client.delete(f"/teams/{team.id}")
    assert response.status_code == 204
    assert client.get(f"/teams/{team.id}").status_code == 404


def test_delete_team_not_found(client):
    response = client.delete("/teams/9999")
    assert response.status_code == 404
