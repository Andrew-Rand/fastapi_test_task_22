"""Create initial questionnaire tables.

Revision ID: 0001_initial
Revises:
Create Date: 2026-10-10
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "reference_items",
        sa.Column("UID", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("Ident", sa.Integer(), nullable=False),
        sa.Column("Cod", sa.Integer(), nullable=True),
        sa.Column("Name", sa.String(length=60), nullable=True),
        sa.Column("Tip2", sa.Integer(), nullable=True),
        sa.Column("FlagDeleted", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("UID"),
    )
    op.create_index("ix_reference_items_Ident", "reference_items", ["Ident"], unique=False)
    op.create_index("ix_reference_items_Cod", "reference_items", ["Cod"], unique=False)

    op.create_table(
        "questions",
        sa.Column("UID", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("Cod", sa.Integer(), nullable=True),
        sa.Column("ID_1", sa.Integer(), nullable=True),
        sa.Column("ID_2", sa.Integer(), nullable=True),
        sa.Column("Count_1", sa.Integer(), nullable=True),
        sa.Column("Count_5", sa.Integer(), nullable=True),
        sa.Column("STR_1", sa.String(length=60), nullable=True),
        sa.Column("Text_1", sa.Text(), nullable=True),
        sa.Column("Boolean_1", sa.Boolean(), nullable=True),
        sa.Column("Count_4", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("UID"),
    )
    op.create_index("ix_questions_Cod", "questions", ["Cod"], unique=False)
    op.create_index("ix_questions_ID_2", "questions", ["ID_2"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_questions_ID_2", table_name="questions")
    op.drop_index("ix_questions_Cod", table_name="questions")
    op.drop_table("questions")
    op.drop_index("ix_reference_items_Cod", table_name="reference_items")
    op.drop_index("ix_reference_items_Ident", table_name="reference_items")
    op.drop_table("reference_items")
