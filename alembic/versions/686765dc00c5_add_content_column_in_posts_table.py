"""add content column in posts table

Revision ID: 686765dc00c5
Revises: 38ec43156c43
Create Date: 2022-05-05 18:15:47.813040

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '686765dc00c5'
down_revision = '38ec43156c43'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
