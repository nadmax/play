import pytest


@pytest.fixture
def company(client):
    return client.post(
        "/companies/", json={"name": "Nintendo", "country": "Japan"}
    ).json()


def test_list_teams_empty(client):
    response = client.get("/teams/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_team(client, company):
    payload = {
        "name": "EPD Group No. 3",
        "specialty": "Development",
        "company_id": company["id"],
    }
    response = client.post("/teams/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "EPD Group No. 3"
    assert data["company_id"] == company["id"]


def test_create_team_company_not_found(client):
    payload = {"name": "Ghost Team", "specialty": "Development", "company_id": 9999}
    response = client.post("/teams/", json=payload)
    assert response.status_code == 404


def test_create_team_missing_field(client, company):
    response = client.post(
        "/teams/", json={"name": "EPD Group No. 3", "company_id": company["id"]}
    )
    assert response.status_code == 422


def test_get_team(client, company):
    created = client.post(
        "/teams/",
        json={"name": "NST", "specialty": "Studio", "company_id": company["id"]},
    ).json()
    response = client.get(f"/teams/{created['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "NST"


def test_get_team_not_found(client):
    response = client.get("/teams/9999")
    assert response.status_code == 404


def test_list_teams(client, company):
    client.post(
        "/teams/",
        json={
            "name": "EPD Group No. 1",
            "specialty": "Development",
            "company_id": company["id"],
        },
    )
    client.post(
        "/teams/",
        json={
            "name": "EPD Group No. 3",
            "specialty": "Development",
            "company_id": company["id"],
        },
    )
    response = client.get("/teams/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_team(client, company):
    created = client.post(
        "/teams/",
        json={"name": "NST", "specialty": "Studio", "company_id": company["id"]},
    ).json()
    response = client.patch(f"/teams/{created['id']}", json={"size": 80})
    assert response.status_code == 200
    assert response.json()["size"] == 80


def test_update_team_company_not_found(client, company):
    created = client.post(
        "/teams/",
        json={"name": "NST", "specialty": "Studio", "company_id": company["id"]},
    ).json()
    response = client.patch(f"/teams/{created['id']}", json={"company_id": 9999})
    assert response.status_code == 404


def test_update_team_not_found(client):
    response = client.patch("/teams/9999", json={"name": "Ghost"})
    assert response.status_code == 404


def test_delete_team(client, company):
    created = client.post(
        "/teams/",
        json={"name": "NST", "specialty": "Studio", "company_id": company["id"]},
    ).json()
    response = client.delete(f"/teams/{created['id']}")
    assert response.status_code == 204
    assert client.get(f"/teams/{created['id']}").status_code == 404


def test_delete_team_not_found(client):
    response = client.delete("/teams/9999")
    assert response.status_code == 404
