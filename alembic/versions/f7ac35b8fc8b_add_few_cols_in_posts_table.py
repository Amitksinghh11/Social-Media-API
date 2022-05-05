"""add few cols in posts table

Revision ID: f7ac35b8fc8b
Revises: 9aeec9c91482
Create Date: 2022-05-05 18:32:20.077536

"""
from cgitb import text
from time import timezone
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7ac35b8fc8b'
down_revision = '9aeec9c91482'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',
                sa.Column('published_at', sa.TIMESTAMP(timezone=True),server_default = sa.text('NOW()'), nullable= False))
    pass


def downgrade():
    op.drop_column('posts','published_at')
    pass
