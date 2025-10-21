"""user added

Revision ID: e444847ed0b5
Revises: 0e36c848a80e
Create Date: 2025-10-21 16:43:51.493706

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e444847ed0b5'
down_revision: Union[str, Sequence[str], None] = '0e36c848a80e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass