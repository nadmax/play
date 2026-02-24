"""
API routes for Team resources.

This module defines all HTTP endpoints related to team management,
including listing, retrieval, creation, update, and deletion.
"""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import orm
from play import database, schemas
from play.services import teams

router = APIRouter(prefix="/teams", tags=["teams"])


@router.get("/", response_model=list[schemas.TeamResponse])
def list_teams(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: orm.Session = Depends(database.get_db),
):
    """
    Retrieve a paginated list of teams.

    Args:
        skip (int): Number of records to skip for pagination.
        limit (int): Maximum number of records to return (1–100).
        db (Session): Database session dependency.

    Returns:
        list[TeamResponse]: List of teams.
    """
    return teams.list_teams(db, skip, limit)


@router.get("/{team_id}", response_model=schemas.TeamResponse)
def get_team(team_id: int, db: orm.Session = Depends(database.get_db)):
    """
    Retrieve a team by its identifier.

    Args:
        team_id (int): Unique identifier of the team.
        db (Session): Database session dependency.

    Returns:
        TeamResponse: The requested team.

    Raises:
        HTTPException: If the team does not exist.
    """
    return teams.get_team(db, team_id)


@router.post(
    "/", response_model=schemas.TeamResponse, status_code=status.HTTP_201_CREATED
)
def create_team(
    payload: schemas.TeamCreate, db: orm.Session = Depends(database.get_db)
):
    """
    Create a new team.

    Args:
        payload (TeamCreate): Team data to create.
        db (Session): Database session dependency.

    Returns:
        TeamResponse: The newly created team.

    Raises:
        HTTPException: If the referenced company does not exist.
    """
    return teams.create_team(db, payload)


@router.patch("/{team_id}", response_model=schemas.TeamResponse)
def update_team(
    team_id: int,
    payload: schemas.TeamUpdate,
    db: orm.Session = Depends(database.get_db),
):
    """
    Partially update an existing team.

    Args:
        team_id (int): Unique identifier of the team.
        payload (TeamUpdate): Fields to update.
        db (Session): Database session dependency.

    Returns:
        TeamResponse: The updated team.

    Raises:
        HTTPException: If the team does not exist.
    """
    return teams.update_team(db, team_id, payload)


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team(team_id: int, db: orm.Session = Depends(database.get_db)):
    """
    Delete a team by its identifier.

    Args:
        team_id (int): Unique identifier of the team.
        db (Session): Database session dependency.

    Returns:
        None: No content is returned on successful deletion.

    Raises:
        HTTPException: If the team does not exist.
    """
    teams.delete_team(db, team_id)
