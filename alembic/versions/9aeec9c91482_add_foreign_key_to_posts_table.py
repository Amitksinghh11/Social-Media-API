"""add foreign key to posts table

Revision ID: 9aeec9c91482
Revises: 1ccc8d5872a7
Create Date: 2022-05-05 18:25:51.147598

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9aeec9c91482'
down_revision = '1ccc8d5872a7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',
                sa.Column('owner_id', sa.Integer(), nullable=False))
    
    op.create_foreign_key('posts_users_fk', source_table= 'posts', referent_table= 'users', local_cols=['owner_id'], remote_cols=['id'] ,ondelete= 'CASCADE')
    pass


def downgrade():
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts','owner_id')
    pass
