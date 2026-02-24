"""
API routes for Company resources.

This module defines all HTTP endpoints related to company management,
including listing, retrieval, creation, update, and deletion.
"""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import orm
from play import database, schemas
from play.services import companies

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("/", response_model=list[schemas.CompanyResponse])
def list_companies(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: orm.Session = Depends(database.get_db),
):
    """
    Retrieve a paginated list of companies.

    Args:
        skip (int): Number of records to skip for pagination.
        limit (int): Maximum number of records to return (1–100).
        db (Session): Database session dependency.

    Returns:
        list[CompanyResponse]: List of companies.
    """
    return companies.list_companies(db, skip, limit)


@router.get("/{company_id}", response_model=schemas.CompanyResponse)
def get_company(company_id: int, db: orm.Session = Depends(database.get_db)):
    """
    Retrieve a company by its identifier.

    Args:
        company_id (int): Unique identifier of the company.
        db (Session): Database session dependency.

    Returns:
        CompanyResponse: The requested company.

    Raises:
        HTTPException: If the company does not exist.
    """
    return companies.get_company(db, company_id)


@router.get("/{company_id}/teams", response_model=schemas.CompanyWithTeams)
def get_company_teams(company_id: int, db: orm.Session = Depends(database.get_db)):
    """
    Retrieve a company along with its associated teams.

    Args:
        company_id (int): Unique identifier of the company.
        db (Session): Database session dependency.

    Returns:
        CompanyWithTeams: Company including its teams.

    Raises:
        HTTPException: If the company does not exist.
    """
    return companies.get_company(db, company_id)


@router.post(
    "/", response_model=schemas.CompanyResponse, status_code=status.HTTP_201_CREATED
)
def create_company(
    payload: schemas.CompanyCreate, db: orm.Session = Depends(database.get_db)
):
    """
    Create a new company.

    Args:
        payload (CompanyCreate): Company data to create.
        db (Session): Database session dependency.

    Returns:
        CompanyResponse: The newly created company.
    """
    return companies.create_company(db, payload)


@router.patch("/{company_id}", response_model=schemas.CompanyResponse)
def update_company(
    company_id: int,
    payload: schemas.CompanyUpdate,
    db: orm.Session = Depends(database.get_db),
):
    """
    Partially update an existing company.

    Args:
        company_id (int): Unique identifier of the company.
        payload (CompanyUpdate): Fields to update.
        db (Session): Database session dependency.

    Returns:
        CompanyResponse: The updated company.

    Raises:
        HTTPException: If the company does not exist.
    """
    return companies.update_company(db, company_id, payload)


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(company_id: int, db: orm.Session = Depends(database.get_db)):
    """
    Delete a company by its identifier.

    Args:
        company_id (int): Unique identifier of the company.
        db (Session): Database session dependency.

    Returns:
        None: No content is returned on successful deletion.

    Raises:
        HTTPException: If the company does not exist.
    """
    companies.delete_company(db, company_id)
