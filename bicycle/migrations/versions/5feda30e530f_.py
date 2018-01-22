"""empty message

Revision ID: 5feda30e530f
Revises: 90bdff5d80d5
Create Date: 2018-01-03 16:43:32.401000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5feda30e530f'
down_revision = '90bdff5d80d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('answer', sa.Column('create_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('answer', 'create_time')
    # ### end Alembic commands ###
