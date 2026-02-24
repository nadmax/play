from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import TeamCreate, TeamUpdate, TeamResponse
from app.services import teams as service

router = APIRouter(prefix="/teams", tags=["teams"])


@router.get("/", response_model=list[TeamResponse])
def list_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.list_teams(db, skip, limit)


@router.get("/{team_id}", response_model=TeamResponse)
def get_team(team_id: int, db: Session = Depends(get_db)):
    return service.get_team(db, team_id)


@router.post("/", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
def create_team(payload: TeamCreate, db: Session = Depends(get_db)):
    return service.create_team(db, payload)


@router.patch("/{team_id}", response_model=TeamResponse)
def update_team(team_id: int, payload: TeamUpdate, db: Session = Depends(get_db)):
    return service.update_team(db, team_id, payload)


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team(team_id: int, db: Session = Depends(get_db)):
    service.delete_team(db, team_id)
