from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas import CompanyCreate, CompanyUpdate, CompanyResponse, CompanyWithTeams
from app.services import companies as service

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("/", response_model=List[CompanyResponse])
def list_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.list_companies(db, skip, limit)


@router.get("/{company_id}", response_model=CompanyWithTeams)
def get_company(company_id: int, db: Session = Depends(get_db)):
    return service.get_company(db, company_id)


@router.post("/", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
def create_company(payload: CompanyCreate, db: Session = Depends(get_db)):
    return service.create_company(db, payload)


@router.patch("/{company_id}", response_model=CompanyResponse)
def update_company(
    company_id: int, payload: CompanyUpdate, db: Session = Depends(get_db)
):
    return service.update_company(db, company_id, payload)


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(company_id: int, db: Session = Depends(get_db)):
    service.delete_company(db, company_id)


@router.get("/{company_id}/teams", response_model=CompanyWithTeams)
def get_company_teams(company_id: int, db: Session = Depends(get_db)):
    return service.get_company(db, company_id)
