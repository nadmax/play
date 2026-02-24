from sqlalchemy import orm, exc
from fastapi import HTTPException, status

from play import models
from play import schemas


def list_companies(db: orm.Session, skip: int = 0, limit: int = 100):
    return db.query(models.Company).offset(skip).limit(limit).all()


def get_company(db: orm.Session, company_id: int):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Company not found"
        )
    return company


def create_company(db: orm.Session, payload: schemas.CompanyCreate):
    try:
        company = models.Company(**payload.model_dump())
        db.add(company)
        db.commit()
        db.refresh(company)
        return company
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Company already exists"
        )


def update_company(db: orm.Session, company_id: int, payload: schemas.CompanyUpdate):
    company = get_company(db, company_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(company, field, value)
    db.commit()
    db.refresh(company)
    return company


def delete_company(db: orm.Session, company_id: int):
    company = get_company(db, company_id)
    db.delete(company)
    db.commit()
