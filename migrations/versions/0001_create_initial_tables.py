"""Create reference_items and questions tables.

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-10-11
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0001_initial_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "reference_items",
        sa.Column("uid", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("ident", sa.Integer(), nullable=False),
        sa.Column("cod", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(length=60), nullable=True),
        sa.Column("tip2", sa.Integer(), nullable=True),
        sa.Column("flag_deleted", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("uid"),
    )
    op.create_index("ix_reference_items_ident", "reference_items", ["ident"], unique=False)
    op.create_index("ix_reference_items_cod", "reference_items", ["cod"], unique=False)

    op.create_table(
        "questions",
        sa.Column("uid", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("cod", sa.Integer(), nullable=True),
        sa.Column("id_1", sa.Integer(), nullable=True),
        sa.Column("id_2", sa.Integer(), nullable=True),
        sa.Column("count_1", sa.Integer(), nullable=True),
        sa.Column("count_5", sa.Integer(), nullable=True),
        sa.Column("str_1", sa.String(length=60), nullable=True),
        sa.Column("text_1", sa.Text(), nullable=True),
        sa.Column("boolean_1", sa.Boolean(), nullable=True),
        sa.Column("count_4", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("uid"),
    )
    op.create_index("ix_questions_cod", "questions", ["cod"], unique=False)
    op.create_index("ix_questions_id_2", "questions", ["id_2"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_questions_id_2", table_name="questions")
    op.drop_index("ix_questions_cod", table_name="questions")
    op.drop_table("questions")
    op.drop_index("ix_reference_items_cod", table_name="reference_items")
    op.drop_index("ix_reference_items_ident", table_name="reference_items")
    op.drop_table("reference_items")