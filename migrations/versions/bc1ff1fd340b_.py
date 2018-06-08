"""empty message

Revision ID: bc1ff1fd340b
Revises: f5578f470e8c
Create Date: 2018-06-07 12:00:31.021817

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc1ff1fd340b'
down_revision = 'f5578f470e8c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('movies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('showname', sa.String(length=100), nullable=True),
    sa.Column('shownameen', sa.String(length=200), nullable=True),
    sa.Column('director', sa.String(length=100), nullable=True),
    sa.Column('leadingRole', sa.String(length=300), nullable=True),
    sa.Column('type', sa.String(length=50), nullable=True),
    sa.Column('country', sa.String(length=100), nullable=True),
    sa.Column('language', sa.String(length=50), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.Column('screeningmodel', sa.String(length=20), nullable=True),
    sa.Column('openday', sa.DateTime(), nullable=True),
    sa.Column('backgroundpicture', sa.String(length=100), nullable=True),
    sa.Column('flag', sa.Integer(), nullable=True),
    sa.Column('isdelete', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('movies')
    # ### end Alembic commands ###
