def test_list_companies_empty(client):
    response = client.get("/companies/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_company(client):
    payload = {"name": "Nintendo", "country": "Japan", "founded_year": 1889}
    response = client.post("/companies/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Nintendo"
    assert data["country"] == "Japan"
    assert data["id"] is not None


def test_create_company_duplicate(client):
    payload = {"name": "Nintendo", "country": "Japan"}
    client.post("/companies/", json=payload)
    response = client.post("/companies/", json=payload)
    assert response.status_code == 409


def test_create_company_missing_field(client):
    response = client.post("/companies/", json={"name": "Nintendo"})
    assert response.status_code == 422


def test_get_company(client):
    created = client.post(
        "/companies/", json={"name": "Ubisoft", "country": "France"}
    ).json()
    response = client.get(f"/companies/{created['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Ubisoft"


def test_get_company_not_found(client):
    response = client.get("/companies/9999")
    assert response.status_code == 404


def test_list_companies(client):
    client.post("/companies/", json={"name": "Nintendo", "country": "Japan"})
    client.post("/companies/", json={"name": "Ubisoft", "country": "France"})
    response = client.get("/companies/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_company(client):
    created = client.post(
        "/companies/", json={"name": "CD Projekt", "country": "Poland"}
    ).json()
    response = client.patch(
        f"/companies/{created['id']}", json={"country": "Poland", "founded_year": 1994}
    )
    assert response.status_code == 200
    assert response.json()["founded_year"] == 1994


def test_update_company_not_found(client):
    response = client.patch("/companies/9999", json={"name": "Ghost"})
    assert response.status_code == 404


def test_delete_company(client):
    created = client.post(
        "/companies/", json={"name": "Valve", "country": "USA"}
    ).json()
    response = client.delete(f"/companies/{created['id']}")
    assert response.status_code == 204
    assert client.get(f"/companies/{created['id']}").status_code == 404


def test_delete_company_not_found(client):
    response = client.delete("/companies/9999")
    assert response.status_code == 404


def test_get_company_teams(client):
    company = client.post(
        "/companies/", json={"name": "FromSoftware", "country": "Japan"}
    ).json()
    client.post(
        "/teams/",
        json={
            "name": "Soulsborne Team",
            "specialty": "Development",
            "company_id": company["id"],
        },
    )
    response = client.get(f"/companies/{company['id']}/teams")
    assert response.status_code == 200
    assert len(response.json()["teams"]) == 1


def test_get_company_teams_not_found(client):
    response = client.get("/companies/9999/teams")
    assert response.status_code == 404
