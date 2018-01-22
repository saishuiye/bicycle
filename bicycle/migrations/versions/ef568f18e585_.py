"""empty message

Revision ID: ef568f18e585
Revises: 5feda30e530f
Create Date: 2018-01-22 19:47:12.842000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ef568f18e585'
down_revision = '5feda30e530f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('file',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuidname', sa.String(length=100), nullable=False),
    sa.Column('realname', sa.String(length=40), nullable=False),
    sa.Column('savepath', sa.String(length=100), nullable=False),
    sa.Column('uploadtime', sa.DateTime(), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column(u'user', sa.Column('email', sa.String(length=26), nullable=False))
    op.drop_column(u'user', 'telephone')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(u'user', sa.Column('telephone', mysql.VARCHAR(length=11), nullable=False))
    op.drop_column(u'user', 'email')
    op.drop_table('file')
    # ### end Alembic commands ###
