"""
Service layer for Team operations.

This module contains business logic related to team management,
including CRUD operations and validation rules.

All database interactions related to teams should go through this layer.
"""

from sqlalchemy import orm, exc
from fastapi import HTTPException, status

from play import models
from play import schemas


def list_teams(db: orm.Session, skip: int = 0, limit: int = 100):
    """
    Retrieve a paginated list of teams.

    Args:
        db (Session): Active database session.
        skip (int): Number of records to skip.
        limit (int): Maximum number of records to return.

    Returns:
        list[Team]: List of team ORM objects.
    """
    return db.query(models.Team).offset(skip).limit(limit).all()


def get_team(db: orm.Session, team_id: int):
    """
    Retrieve a team by its identifier.

    Args:
        db (Session): Active database session.
        team_id (int): Unique identifier of the team.

    Returns:
        Team: The requested team ORM object.

    Raises:
        HTTPException: If the team does not exist.
    """
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found"
        )
    return team


def _check_company_exists(db: orm.Session, company_id: int):
    """
    Ensure that a company exists.

    Args:
        db (Session): Active database session.
        company_id (int): Identifier of the company.

    Raises:
        HTTPException: If the company does not exist.
    """
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Company not found"
        )


def create_team(db: orm.Session, payload: schemas.TeamCreate):
    """
    Create a new team.

    Args:
        db (Session): Active database session.
        payload (TeamCreate): Validated team creation data.

    Returns:
        Team: The newly created team ORM object.

    Raises:
        HTTPException:
            - 404 if the referenced company does not exist.
    """
    try:
        team = models.Team(**payload.model_dump())
        db.add(team)
        db.commit()
        db.refresh(team)
        return team
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(status_code=404, detail="Company not found")


def update_team(db: orm.Session, team_id: int, payload: schemas.TeamUpdate):
    """
    Update an existing team.

    Applies partial updates based on provided fields.

    Args:
        db (Session): Active database session.
        team_id (int): Identifier of the team to update.
        payload (TeamUpdate): Fields to update.

    Returns:
        Team: The updated team ORM object.

    Raises:
        HTTPException:
            - 404 if the team does not exist.
            - 404 if the updated company reference does not exist.
    """
    try:
        team = (
            db.query(models.Team)
            .filter(models.Team.id == team_id)
            .with_for_update()
            .first()
        )
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")

        data = payload.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(team, field, value)

        db.commit()
        db.refresh(team)
        return team
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(status_code=404, detail="Company not found")


def delete_team(db: orm.Session, team_id: int):
    """
    Delete a team by its identifier.

    Args:
        db (Session): Active database session.
        team_id (int): Identifier of the team to delete.

    Raises:
        HTTPException: If the team does not exist.
    """
    team = get_team(db, team_id)
    db.delete(team)
    db.commit()
