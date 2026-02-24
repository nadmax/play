from fastapi import APIRouter
from app.routers import companies, teams

router = APIRouter()

router.include_router(companies.router)
router.include_router(teams.router)
