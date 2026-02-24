"""
Service layer for Company operations.

This module contains business logic related to company management,
including CRUD operations and validation handling.

All database interactions related to companies should go through this layer.
"""

from sqlalchemy import orm, exc
from fastapi import HTTPException, status

from play import models
from play import schemas


def list_companies(db: orm.Session, skip: int = 0, limit: int = 100):
    """
    Retrieve a paginated list of companies.

    Args:
        db (Session): Active database session.
        skip (int): Number of records to skip.
        limit (int): Maximum number of records to return.

    Returns:
        list[Company]: List of company ORM objects.
    """
    return db.query(models.Company).offset(skip).limit(limit).all()


def get_company(db: orm.Session, company_id: int):
    """
    Retrieve a company by its identifier.

    Args:
        db (Session): Active database session.
        company_id (int): Unique identifier of the company.

    Returns:
        Company: The requested company ORM object.

    Raises:
        HTTPException: If the company does not exist.
    """
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Company not found"
        )
    return company


def create_company(db: orm.Session, payload: schemas.CompanyCreate):
    """
    Create a new company.

    Args:
        db (Session): Active database session.
        payload (CompanyCreate): Validated company creation data.

    Returns:
        Company: The newly created company ORM object.

    Raises:
        HTTPException:
            - 409 if a company with the same unique constraints already exists.
    """
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
    """
    Update an existing company.

    Applies partial updates based on provided fields.

    Args:
        db (Session): Active database session.
        company_id (int): Identifier of the company to update.
        payload (CompanyUpdate): Fields to update.

    Returns:
        Company: The updated company ORM object.

    Raises:
        HTTPException:
            - 404 if the company does not exist.
    """
    company = get_company(db, company_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(company, field, value)
    db.commit()
    db.refresh(company)
    return company


def delete_company(db: orm.Session, company_id: int):
    """
    Delete a company by its identifier.

    Args:
        db (Session): Active database session.
        company_id (int): Identifier of the company to delete.

    Raises:
        HTTPException:
            - 404 if the company does not exist.
    """
    company = get_company(db, company_id)
    db.delete(company)
    db.commit()
