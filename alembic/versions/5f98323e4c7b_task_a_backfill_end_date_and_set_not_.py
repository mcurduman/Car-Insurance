"""Task A: backfill end_date and set NOT NULL

Revision ID: 5f98323e4c7b
Revises: ea6bf56b29e4
Create Date: 2025-10-22 22:31:06.947876

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f98323e4c7b'
down_revision: Union[str, Sequence[str], None] = 'ea6bf56b29e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    bind = op.get_bind()
    dialect = bind.dialect.name  # 'postgresql', 'sqlite', etc.

    # 1) Backfill end_date where NULL
    if dialect == "postgresql":
        # INTERVAL '1 year' funcționează corect pe DATE (returnează DATE)
        op.execute(
            sa.text(
                """
                UPDATE insurance_policy
                SET end_date = start_date + INTERVAL '1 year'
                WHERE end_date IS NULL
                """
            )
        )
    elif dialect == "sqlite":
        op.execute(
            sa.text(
                """
                UPDATE insurance_policy
                SET end_date = DATE(start_date, '+1 year')
                WHERE end_date IS NULL
                """
            )
        )
    else:
        op.execute(
            sa.text(
                """
                UPDATE insurance_policy
                SET end_date = start_date
                WHERE end_date IS NULL
                """
            )
        )

    # 2) SET NOT NULL pe coloana end_date
    if dialect == "sqlite":
        with op.batch_alter_table("insurance_policy") as batch_op:
            batch_op.alter_column(
                "end_date",
                existing_type=sa.Date(),
                nullable=False,
            )
    else:
        op.alter_column(
            "insurance_policy",
            "end_date",
            existing_type=sa.Date(),
            nullable=False,
        )


def downgrade():
    bind = op.get_bind()
    dialect = bind.dialect.name

    if dialect == "sqlite":
        with op.batch_alter_table("insurance_policy") as batch_op:
            batch_op.alter_column(
                "end_date",
                existing_type=sa.Date(),
                nullable=True,
            )
    else:
        op.alter_column(
            "insurance_policy",
            "end_date",
            existing_type=sa.Date(),
            nullable=True,
        )