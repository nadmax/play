"""
Application entry point for the Play API.

This module initializes the FastAPI application, registers routers,
and exposes a root health endpoint.
"""

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
    """
    Response schema for the root health endpoint.

    Attributes:
        name (str): Name of the API.
        version (str): Current API version.
        docs (str): URL path to the interactive API documentation.
    """

    name: str
    version: str
    docs: str


@app.get("/", tags=["root"], response_model=HealthResponse)
def root():
    """
    Root health endpoint.

    Returns basic metadata about the API, including its name,
    version, and documentation URL.

    Returns:
        HealthResponse: API metadata information.
    """
    return HealthResponse(name="Play API", version="1.0.0", docs="/docs")
