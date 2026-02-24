from fastapi import APIRouter, Depends, status
from sqlalchemy import orm

from play import database, schemas
from play.services import companies

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("/", response_model=list[schemas.CompanyResponse])
def list_companies(
    skip: int = 0, limit: int = 100, db: orm.Session = Depends(database.get_db)
):
    return companies.list_companies(db, skip, limit)


@router.get("/{company_id}", response_model=schemas.CompanyWithTeams)
def get_company(company_id: int, db: orm.Session = Depends(database.get_db)):
    return companies.get_company(db, company_id)


@router.post(
    "/", response_model=schemas.CompanyResponse, status_code=status.HTTP_201_CREATED
)
def create_company(
    payload: schemas.CompanyCreate, db: orm.Session = Depends(database.get_db)
):
    return companies.create_company(db, payload)


@router.patch("/{company_id}", response_model=schemas.CompanyResponse)
def update_company(
    company_id: int,
    payload: schemas.CompanyUpdate,
    db: orm.Session = Depends(database.get_db),
):
    return companies.update_company(db, company_id, payload)


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(company_id: int, db: orm.Session = Depends(database.get_db)):
    companies.delete_company(db, company_id)


@router.get("/{company_id}/teams", response_model=schemas.CompanyWithTeams)
def get_company_teams(company_id: int, db: orm.Session = Depends(database.get_db)):
    return companies.get_company(db, company_id)
