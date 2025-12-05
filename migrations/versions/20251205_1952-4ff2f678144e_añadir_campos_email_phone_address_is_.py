"""añadir campos email, phone, address, is_active a User

Revision ID: 4ff2f678144e
Revises: c173a78d47eb
Create Date: 2025-12-05 19:52:51.160134

"""
from typing import Sequence, Union

import advanced_alchemy
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = '4ff2f678144e'
down_revision: Union[str, Sequence[str], None] = 'c173a78d47eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("email", sa.String(), nullable=False))
    op.add_column("users", sa.Column("phone", sa.String(), nullable=True))
    op.add_column("users", sa.Column("address", sa.String(), nullable=True))
    op.add_column("users", sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"))
    op.create_unique_constraint("uq_users_email", "users", ["email"])


def downgrade() -> None:
    op.drop_constraint("uq_users_email", "users", type_="unique")
    op.drop_column("users", "is_active")
    op.drop_column("users", "address")
    op.drop_column("users", "phone")
    op.drop_column("users", "email")

