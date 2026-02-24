import pytest
from fastapi import HTTPException

from play import models, schemas
from play.services import companies


def make_company(db, name="Nintendo", country="Japan"):
    company = models.Company(name=name, country=country)
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


def test_list_companies_empty(db):
    assert companies.list_companies(db) == []


def test_list_companies_returns_all(db):
    make_company(db, name="Nintendo")
    make_company(db, name="Sega")
    result = companies.list_companies(db)
    assert len(result) == 2


def test_list_companies_skip_and_limit(db):
    for name in ["A", "B", "C"]:
        make_company(db, name=name)
    result = companies.list_companies(db, skip=1, limit=1)
    assert len(result) == 1
    assert result[0].name == "B"


def test_get_company_returns_company(db):
    company = make_company(db)
    result = companies.get_company(db, company.id)
    assert result.id == company.id
    assert result.name == "Nintendo"


def test_get_company_not_found(db):
    with pytest.raises(HTTPException) as exc:
        companies.get_company(db, 999)
    assert exc.value.status_code == 404
    assert exc.value.detail == "Company not found"


def test_create_company_success(db):
    payload = schemas.CompanyCreate(name="Capcom", country="Japan")
    result = companies.create_company(db, payload)
    assert result.id is not None
    assert result.name == "Capcom"


def test_create_company_duplicate_raises_conflict(db):
    make_company(db, name="Capcom")
    payload = schemas.CompanyCreate(name="Capcom", country="Japan")
    with pytest.raises(HTTPException) as exc:
        companies.create_company(db, payload)
    assert exc.value.status_code == 409
    assert exc.value.detail == "Company already exists"


def test_update_company_success(db):
    company = make_company(db)
    payload = schemas.CompanyUpdate(country="USA")
    result = companies.update_company(db, company.id, payload)
    assert result.country == "USA"
    assert result.name == "Nintendo"


def test_update_company_not_found(db):
    payload = schemas.CompanyUpdate(country="USA")
    with pytest.raises(HTTPException) as exc:
        companies.update_company(db, 999, payload)
    assert exc.value.status_code == 404


def test_delete_company_success(db):
    company = make_company(db)
    companies.delete_company(db, company.id)
    with pytest.raises(HTTPException):
        companies.get_company(db, company.id)


def test_delete_company_not_found(db):
    with pytest.raises(HTTPException) as exc:
        companies.delete_company(db, 999)
    assert exc.value.status_code == 404
