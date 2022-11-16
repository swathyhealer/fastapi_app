"""add column description to books

Revision ID: 2e5dc27d0f9c
Revises: fc2482bcf572
Create Date: 2022-11-11 15:43:37.640070

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "2e5dc27d0f9c"
down_revision = "fc2482bcf572"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("books", sa.Column("Description", sa.String(), nullable=True))
    # op.add_column(
    #     'users',
    #     sa.Column('is_admin', sa.Boolean(), nullable=True)
    # )
    # op.execute("UPDATE users SET is_admin = false")
    # op.alter_column('users', 'is_admin', nullable=False)


def downgrade() -> None:
    op.drop_column("books", "Description")
