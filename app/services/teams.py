from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models import Team, Company
from app.schemas import TeamCreate, TeamUpdate


def list_teams(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Team).offset(skip).limit(limit).all()


def get_team(db: Session, team_id: int):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found"
        )
    return team


def _check_company_exists(db: Session, company_id: int):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Company not found"
        )


def create_team(db: Session, payload: TeamCreate):
    _check_company_exists(db, payload.company_id)
    team = Team(**payload.model_dump())
    db.add(team)
    db.commit()
    db.refresh(team)
    return team


def update_team(db: Session, team_id: int, payload: TeamUpdate):
    team = get_team(db, team_id)
    data = payload.model_dump(exclude_unset=True)
    if "company_id" in data:
        _check_company_exists(db, data["company_id"])
    for field, value in data.items():
        setattr(team, field, value)
    db.commit()
    db.refresh(team)
    return team


def delete_team(db: Session, team_id: int):
    team = get_team(db, team_id)
    db.delete(team)
    db.commit()
