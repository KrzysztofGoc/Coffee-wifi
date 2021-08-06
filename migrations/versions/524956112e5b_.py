"""empty message

Revision ID: 524956112e5b
Revises: 
Create Date: 2021-08-05 12:47:28.440052

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '524956112e5b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cafe',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('location', sa.String(length=250), nullable=False),
    sa.Column('open_time', sa.Time(), nullable=False),
    sa.Column('close_time', sa.Time(), nullable=False),
    sa.Column('coffee_quality', sa.String(length=250), nullable=False),
    sa.Column('wifi_speed', sa.String(length=250), nullable=False),
    sa.Column('power_socket', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.VARCHAR(length=100), nullable=True),
    sa.Column('password', sa.VARCHAR(length=250), nullable=True),
    sa.Column('name', sa.VARCHAR(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('cafe')
    # ### end Alembic commands ###