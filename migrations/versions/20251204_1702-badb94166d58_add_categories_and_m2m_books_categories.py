"""add categories and m2m books_categories

Revision ID: badb94166d58
Revises: acc8ae75f9e8
Create Date: 2025-12-04 17:02:12.854492

"""
from typing import Sequence, Union

import advanced_alchemy
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'badb94166d58'
down_revision: Union[str, Sequence[str], None] = 'acc8ae75f9e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "categories",
        sa.Column("id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("created_at", advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),
        sa.Column("updated_at", advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_categories")),
        sa.UniqueConstraint("name", name=op.f("uq_categories_name")),
    )

    op.create_table(
        "books_categories",
        sa.Column("book_id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), primary_key=True),
        sa.Column("category_id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), primary_key=True),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], name=op.f("fk_books_categories_book")),
        sa.ForeignKeyConstraint(["category_id"], ["categories.id"], name=op.f("fk_books_categories_category")),
    )

def downgrade():
    op.drop_table("books_categories")
    op.drop_table("categories")