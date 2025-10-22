"""Task d change logged_expiry_at to timestamptz

Revision ID: c40fdee08f23
Revises: 5f98323e4c7b
Create Date: 2025-10-22 23:06:57.890363

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c40fdee08f23'
down_revision: Union[str, Sequence[str], None] = '5f98323e4c7b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
