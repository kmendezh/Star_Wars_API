"""empty message

Revision ID: ae87317c1721
Revises: 762402052503
Create Date: 2021-04-01 01:38:50.120085

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae87317c1721'
down_revision = '762402052503'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('people',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('height', sa.Integer(), nullable=True),
    sa.Column('mass', sa.Integer(), nullable=True),
    sa.Column('hair_color', sa.String(length=30), nullable=True),
    sa.Column('skin_color', sa.String(length=30), nullable=True),
    sa.Column('eye_color', sa.String(length=30), nullable=True),
    sa.Column('birth_year', sa.Integer(), nullable=True),
    sa.Column('gender', sa.String(length=30), nullable=True),
    sa.Column('created', sa.String(length=30), nullable=True),
    sa.Column('edited', sa.String(length=30), nullable=True),
    sa.Column('homeworld', sa.String(length=30), nullable=True),
    sa.Column('description', sa.String(length=30), nullable=True),
    sa.Column('url', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('people')
    # ### end Alembic commands ###
