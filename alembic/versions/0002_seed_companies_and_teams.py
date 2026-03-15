"""seed companies and teams

Revision ID: 0002
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0002"
down_revision: Union[str, Sequence[str], None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

COMPANIES: list[dict] = [
    {
        "name": "Nintendo",
        "country": "Japan",
        "founded_year": 1889,
        "website": "https://www.nintendo.com",
        "description": (
            "Japanese multinational video game company known for iconic "
            "franchises like Mario, Zelda, and Pokémon."
        ),
    },
    {
        "name": "Ubisoft",
        "country": "France",
        "founded_year": 1986,
        "website": "https://www.ubisoft.com",
        "description": (
            "French video game publisher known for Assassin's Creed, "
            "Far Cry, and Rainbow Six."
        ),
    },
    {
        "name": "CD Projekt",
        "country": "Poland",
        "founded_year": 1994,
        "website": "https://www.cdprojekt.com",
        "description": (
            "Polish game developer and publisher known for The Witcher "
            "series and Cyberpunk 2077."
        ),
    },
    {
        "name": "Valve Corporation",
        "country": "USA",
        "founded_year": 1996,
        "website": "https://www.valvesoftware.com",
        "description": (
            "American video game developer and digital distribution company, "
            "creator of Steam, Half-Life, and Dota 2."
        ),
    },
    {
        "name": "FromSoftware",
        "country": "Japan",
        "founded_year": 1986,
        "website": "https://www.fromsoftware.jp",
        "description": (
            "Japanese video game developer known for Souls series, "
            "Sekiro, and Elden Ring."
        ),
    },
]

TEAMS: list[dict] = [
    {
        "name": "EPD Production Group No. 1",
        "specialty": "Development",
        "size": 120,
        "description": "Responsible for Nintendo Switch sports and ring-fit games.",
        "company_name": "Nintendo",
    },
    {
        "name": "EPD Production Group No. 3",
        "specialty": "Development",
        "size": 200,
        "description": "Developed Breath of the Wild and Tears of the Kingdom.",
        "company_name": "Nintendo",
    },
    {
        "name": "NST",
        "specialty": "Studio",
        "size": 80,
        "description": "Nintendo Software Technology, US-based dev team.",
        "company_name": "Nintendo",
    },
    {
        "name": "Ubisoft Montreal",
        "specialty": "Development",
        "size": 4000,
        "description": "Largest game studio in the world, led many AAA titles.",
        "company_name": "Ubisoft",
    },
    {
        "name": "Ubisoft Paris",
        "specialty": "Development",
        "size": 800,
        "description": "Co-developed multiple Assassin's Creed titles.",
        "company_name": "Ubisoft",
    },
    {
        "name": "Ubisoft Online Services",
        "specialty": "Infrastructure",
        "size": 300,
        "description": "Handles all online infrastructure and live services.",
        "company_name": "Ubisoft",
    },
    {
        "name": "CD Projekt RED",
        "specialty": "Development",
        "size": 1200,
        "description": "Main development studio behind The Witcher and Cyberpunk 2077.",
        "company_name": "CD Projekt",
    },
    {
        "name": "GOG",
        "specialty": "Publishing",
        "size": 250,
        "description": "Digital game distribution platform focusing on DRM-free games.",
        "company_name": "CD Projekt",
    },
    {
        "name": "QA Department",
        "specialty": "Quality Assurance",
        "size": 300,
        "description": "Internal QA team for all CD Projekt titles.",
        "company_name": "CD Projekt",
    },
    {
        "name": "Steam Platform Team",
        "specialty": "Platform",
        "size": 200,
        "description": "Develops and maintains the Steam gaming platform.",
        "company_name": "Valve Corporation",
    },
    {
        "name": "Hardware Team",
        "specialty": "Hardware",
        "size": 150,
        "description": "Responsible for Steam Deck and Index VR headset.",
        "company_name": "Valve Corporation",
    },
    {
        "name": "Game Development",
        "specialty": "Development",
        "size": 100,
        "description": "Works on Valve's own game titles.",
        "company_name": "Valve Corporation",
    },
    {
        "name": "Soulsborne Team",
        "specialty": "Development",
        "size": 300,
        "description": "Core team behind Dark Souls, Bloodborne, and Elden Ring.",
        "company_name": "FromSoftware",
    },
    {
        "name": "Armored Core Team",
        "specialty": "Development",
        "size": 150,
        "description": "Team dedicated to the Armored Core mecha series.",
        "company_name": "FromSoftware",
    },
    {
        "name": "Sound & Music",
        "specialty": "Audio",
        "size": 40,
        "description": "Creates the iconic soundscapes and music of FromSoftware games.",
        "company_name": "FromSoftware",
    },
]


def upgrade() -> None:
    """Insert seed companies and teams, skipping rows that already exist."""

    bind = op.get_bind()

    companies_table = sa.table(
        "companies",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String),
        sa.column("country", sa.String),
        sa.column("founded_year", sa.Integer),
        sa.column("website", sa.String),
        sa.column("description", sa.Text),
    )
    teams_table = sa.table(
        "teams",
        sa.column("name", sa.String),
        sa.column("specialty", sa.String),
        sa.column("size", sa.Integer),
        sa.column("description", sa.Text),
        sa.column("company_id", sa.Integer),
    )

    existing_names: set[str] = {
        row[0] for row in bind.execute(sa.select(companies_table.c.name)).fetchall()
    }

    new_companies = [c for c in COMPANIES if c["name"] not in existing_names]
    if new_companies:
        bind.execute(companies_table.insert(), new_companies)

    company_id_by_name: dict[str, int] = {
        row[1]: row[0]
        for row in bind.execute(
            sa.select(companies_table.c.id, companies_table.c.name)
        ).fetchall()
    }

    existing_teams: set[tuple[str, int]] = {
        (row[0], row[1])
        for row in bind.execute(
            sa.select(teams_table.c.name, teams_table.c.company_id)
        ).fetchall()
    }

    new_teams = []
    for team in TEAMS:
        company_id = company_id_by_name[team["company_name"]]
        if (team["name"], company_id) not in existing_teams:
            new_teams.append(
                {
                    "name": team["name"],
                    "specialty": team["specialty"],
                    "size": team["size"],
                    "description": team["description"],
                    "company_id": company_id,
                }
            )

    if new_teams:
        bind.execute(teams_table.insert(), new_teams)


def downgrade() -> None:
    """Remove the seed rows (teams first, then companies)."""

    bind = op.get_bind()

    companies_table = sa.table("companies", sa.column("name", sa.String))
    teams_table = sa.table("teams", sa.column("company_id", sa.Integer))
    companies_id_table = sa.table(
        "companies",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String),
    )

    seeded_names = [c["name"] for c in COMPANIES]

    rows = bind.execute(
        sa.select(companies_id_table.c.id).where(
            companies_id_table.c.name.in_(seeded_names)
        )
    ).fetchall()
    seeded_ids = [row[0] for row in rows]

    if seeded_ids:
        bind.execute(
            teams_table.delete().where(teams_table.c.company_id.in_(seeded_ids))
        )

    bind.execute(
        companies_table.delete().where(companies_table.c.name.in_(seeded_names))
    )
