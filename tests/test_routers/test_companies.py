from app import models


def make_company(db, name="Nintendo", country="Japan", founded_year=None):
    company = models.Company(name=name, country=country, founded_year=founded_year)
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


def test_list_companies_empty(client):
    response = client.get("/companies/")
    assert response.status_code == 200
    assert response.json() == []


def test_list_companies(client, db):
    make_company(db, name="Nintendo")
    make_company(db, name="Ubisoft", country="France")
    response = client.get("/companies/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_company(client, db):
    company = make_company(db, name="Ubisoft", country="France")
    response = client.get(f"/companies/{company.id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Ubisoft"


def test_get_company_not_found(client):
    response = client.get("/companies/9999")
    assert response.status_code == 404


def test_create_company(client):
    payload = {"name": "Nintendo", "country": "Japan", "founded_year": 1889}
    response = client.post("/companies/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Nintendo"
    assert data["country"] == "Japan"
    assert data["id"] is not None


def test_create_company_duplicate(client, db):
    make_company(db, name="Nintendo")
    response = client.post("/companies/", json={"name": "Nintendo", "country": "Japan"})
    assert response.status_code == 409


def test_create_company_missing_field(client):
    response = client.post("/companies/", json={"name": "Nintendo"})
    assert response.status_code == 422


def test_update_company(client, db):
    company = make_company(db, name="CD Projekt", country="Poland")
    response = client.patch(
        f"/companies/{company.id}", json={"country": "Poland", "founded_year": 1994}
    )
    assert response.status_code == 200
    assert response.json()["founded_year"] == 1994


def test_update_company_not_found(client):
    response = client.patch("/companies/9999", json={"name": "Ghost"})
    assert response.status_code == 404


def test_delete_company(client, db):
    company = make_company(db, name="Valve", country="USA")
    response = client.delete(f"/companies/{company.id}")
    assert response.status_code == 204
    assert client.get(f"/companies/{company.id}").status_code == 404


def test_delete_company_not_found(client):
    response = client.delete("/companies/9999")
    assert response.status_code == 404


def test_get_company_teams(client, db):
    from app.models import Team

    company = make_company(db, name="FromSoftware")
    team = Team(name="Soulsborne Team", specialty="Development", company_id=company.id)
    db.add(team)
    db.commit()
    response = client.get(f"/companies/{company.id}/teams")
    assert response.status_code == 200
    assert len(response.json()["teams"]) == 1


def test_get_company_teams_not_found(client):
    response = client.get("/companies/9999/teams")
    assert response.status_code == 404
