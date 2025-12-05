"""añadir campos de inventario y descripción al modelo Book

Revision ID: c173a78d47eb
Revises: c98fcde95f48
Create Date: 2025-12-05 19:38:12.217448

"""
from typing import Sequence, Union

import advanced_alchemy
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'c173a78d47eb'
down_revision: Union[str, Sequence[str], None] = 'c98fcde95f48'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("books", sa.Column("stock", sa.Integer(), nullable=False, server_default="1"))
    op.add_column("books", sa.Column("description", sa.String(), nullable=True))
    op.add_column("books", sa.Column("language", sa.String(length=2), nullable=False, server_default="es"))
    op.add_column("books", sa.Column("publisher", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("books", "publisher")
    op.drop_column("books", "language")
    op.drop_column("books", "description")
    op.drop_column("books", "stock")

