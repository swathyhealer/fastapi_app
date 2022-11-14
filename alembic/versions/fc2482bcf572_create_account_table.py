"""create account table

Revision ID: fc2482bcf572
Revises: 
Create Date: 2022-11-11 15:36:10.742379

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc2482bcf572'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('books', sa.Column('status', sa.String))


def downgrade() -> None:
     op.drop_column('books','status')
   
