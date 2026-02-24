from sqlalchemy import orm
from fastapi import HTTPException, status

from app import models
from app import schemas


def list_teams(db: orm.Session, skip: int = 0, limit: int = 100):
    return db.query(models.Team).offset(skip).limit(limit).all()


def get_team(db: orm.Session, team_id: int):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found"
        )
    return team


def _check_company_exists(db: orm.Session, company_id: int):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Company not found"
        )


def create_team(db: orm.Session, payload: schemas.TeamCreate):
    _check_company_exists(db, payload.company_id)
    team = models.Team(**payload.model_dump())
    db.add(team)
    db.commit()
    db.refresh(team)
    return team


def update_team(db: orm.Session, team_id: int, payload: schemas.TeamUpdate):
    team = get_team(db, team_id)
    _check_company_exists(db, payload.company_id)
    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(team, field, value)
    db.commit()
    db.refresh(team)
    return team


def delete_team(db: orm.Session, team_id: int):
    team = get_team(db, team_id)
    db.delete(team)
    db.commit()
