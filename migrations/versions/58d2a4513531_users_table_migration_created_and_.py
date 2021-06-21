"""Users table migration: created and updated cols

Revision ID: 58d2a4513531
Revises: 693850203971
Create Date: 2021-06-14 16:20:38.496882

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58d2a4513531'
down_revision = '693850203971'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('created_on', sa.DateTime(), nullable=False))
    op.add_column('users', sa.Column('updated_on', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'updated_on')
    op.drop_column('users', 'created_on')
    # ### end Alembic commands ###