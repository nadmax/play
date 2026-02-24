from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager
from play.routers import companies, teams


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="Play",
    description="An API to manage videogame companies with their teams.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(companies.router)
app.include_router(teams.router)


class HealthResponse(BaseModel):
    name: str
    version: str
    docs: str


@app.get("/", tags=["root"], response_model=HealthResponse)
def root():
    return HealthResponse(name="Play API", version="1.0.0", docs="/docs")
