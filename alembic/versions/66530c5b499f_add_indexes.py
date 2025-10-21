"""Add indexes

Revision ID: 66530c5b499f
Revises: 1f4b3c7fbaba
Create Date: 2025-10-20 17:51:46.154125

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '66530c5b499f'
down_revision: Union[str, Sequence[str], None] = '1f4b3c7fbaba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

from alembic import op

def upgrade():
    op.create_index('ix_car_vin', 'car', ['vin'], unique=True)
    op.create_index('ix_insurance_policy_car_id_start_date_end_date', 'insurance_policy', ['car_id', 'start_date', 'end_date'])
    op.create_index('ix_claim_car_id_claim_date', 'claim', ['car_id', 'claim_date'])

def downgrade():
    op.drop_index('ix_claim_car_id_claim_date', table_name='claim')
    op.drop_index('ix_insurance_policy_car_id_start_date_end_date', table_name='insurance_policy')
    op.drop_index('ix_car_vin', table_name='car')
