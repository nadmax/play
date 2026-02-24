![CI](https://github.com/nadmax/play/actions/workflows/ci.yaml/badge.svg) ![CD](https://github.com/nadmax/play/actions/workflows/cd.yaml/badge.svg)

# Play

Play is an API that manages videogame companies with their teams.

## Getting started

### Prerequisites

- Docker

### Run the project

1. Clone the repository

```sh
git clone https://github.com/nadmax/play.git
cd play
```

2. Configure environment variables

```sh
cp .env.example .env
```

Edit `.env` with your own values.  

3. Start the project

```sh
docker compose up -d --build
```

The API is available at [http://localhost:8080](http://localhost:8080).  
To explore and test all available endpoints interactively, open [http://localhost:8080/docs](http://localhost:8080/docs).

The database is automatically created and seeded with real videogame companies and their teams on first startup.

## Environment variables

### Database

| Variable | Description | Default |
|---|---|---|
| `POSTGRES_USER` | PostgreSQL username | - |
| `POSTGRES_HOST` | PostgreSQL host | `db` |
| `POSTGRES_PORT` | PostgreSQL port | `5432` |
| `POSTGRES_PASSWORD` | PostgreSQL password | - |
| `POSTGRES_DB` | PostgreSQL database name | - |

### API

| Variable | Description | Default |
|---|---|---|
| `API_PORT` | Port the API listens on | `8080` |

## Links

- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Docker](https://www.docker.com/)
