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
    return teams.list_teams(db, skip, limit)


@router.get("/{team_id}", response_model=schemas.TeamResponse)
def get_team(team_id: int, db: orm.Session = Depends(database.get_db)):
    return teams.get_team(db, team_id)


@router.post(
    "/", response_model=schemas.TeamResponse, status_code=status.HTTP_201_CREATED
)
def create_team(
    payload: schemas.TeamCreate, db: orm.Session = Depends(database.get_db)
):
    return teams.create_team(db, payload)


@router.patch("/{team_id}", response_model=schemas.TeamResponse)
def update_team(
    team_id: int,
    payload: schemas.TeamUpdate,
    db: orm.Session = Depends(database.get_db),
):
    return teams.update_team(db, team_id, payload)


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team(team_id: int, db: orm.Session = Depends(database.get_db)):
    teams.delete_team(db, team_id)

