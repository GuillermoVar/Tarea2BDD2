"""add due_date fine_amount and status to loans

Revision ID: f817f96fe6ec
Revises: 4ff2f678144e
Create Date: 2025-12-05 20:23:32.282295

"""
from typing import Sequence, Union

import advanced_alchemy
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'f817f96fe6ec'
down_revision: Union[str, Sequence[str], None] = '4ff2f678144e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # crear enum LoanStatus (Postgres)
    loan_status = sa.Enum("ACTIVE", "RETURNED", "OVERDUE", name="loanstatus")
    loan_status.create(op.get_bind(), checkfirst=True)

    op.add_column("loans", sa.Column("due_date", sa.Date(), nullable=False))
    op.add_column("loans", sa.Column("fine_amount", sa.Numeric(10, 2), nullable=True))
    op.add_column("loans", sa.Column("status", loan_status, nullable=False, server_default="ACTIVE"))


def downgrade() -> None:
    op.drop_column("loans", "status")
    op.drop_column("loans", "fine_amount")
    op.drop_column("loans", "due_date")

    # eliminar enum
    loan_status = sa.Enum(name="loanstatus")
    loan_status.drop(op.get_bind(), checkfirst=True)