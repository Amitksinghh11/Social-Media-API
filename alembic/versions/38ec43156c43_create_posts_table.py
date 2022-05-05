"""create posts table

Revision ID: 38ec43156c43
Revises: 
Create Date: 2022-05-05 18:06:51.090618

"""
import string
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38ec43156c43'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable = False, primary_key = True),
                            sa.Column('title', sa.String(), nullable = False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
