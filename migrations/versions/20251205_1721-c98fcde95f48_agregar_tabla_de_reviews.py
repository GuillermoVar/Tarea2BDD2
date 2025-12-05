"""agregar tabla de reviews

Revision ID: c98fcde95f48
Revises: badb94166d58
Create Date: 2025-12-05 17:21:37.715600

"""
from typing import Sequence, Union

import advanced_alchemy
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'c98fcde95f48'
down_revision: Union[str, Sequence[str], None] = 'badb94166d58'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "reviews",
        sa.Column("id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("comment", sa.String(), nullable=False),
        sa.Column("review_date", sa.Date(), nullable=False),
        sa.Column("user_id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False),
        sa.Column("book_id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False),
        sa.Column("created_at", advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),
        sa.Column("updated_at", advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),

        # Definiciones de restricciones
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("reviews")