"""create companies and teams tables

Revision ID: 0001
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the companies and teams tables with their indexes."""

    op.create_table(
        "companies",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("country", sa.String(100), nullable=False),
        sa.Column("founded_year", sa.Integer(), nullable=True),
        sa.Column("website", sa.String(255), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.UniqueConstraint("name", name="uq_companies_name"),
    )
    op.create_index("idx_companies_name", "companies", ["name"])

    op.create_table(
        "teams",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("specialty", sa.String(100), nullable=False),
        sa.Column("size", sa.Integer(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "company_id",
            sa.Integer(),
            sa.ForeignKey("companies.id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    op.create_index("idx_teams_name", "teams", ["name"])
    op.create_index("idx_teams_company_id", "teams", ["company_id"])


def downgrade() -> None:
    """Drop the teams and companies tables (order matters: FK child first)."""

    op.drop_index("idx_teams_company_id", table_name="teams")
    op.drop_index("idx_teams_name", table_name="teams")
    op.drop_table("teams")

    op.drop_index("idx_companies_name", table_name="companies")
    op.drop_table("companies")
