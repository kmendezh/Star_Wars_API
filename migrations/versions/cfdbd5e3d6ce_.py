"""empty message

Revision ID: cfdbd5e3d6ce
Revises: 869fa50c379b
Create Date: 2021-04-01 02:43:51.112487

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'cfdbd5e3d6ce'
down_revision = '869fa50c379b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('characters',
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
    op.drop_table('people')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('people',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=30), nullable=False),
    sa.Column('height', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('mass', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('hair_color', mysql.VARCHAR(length=30), nullable=True),
    sa.Column('skin_color', mysql.VARCHAR(length=30), nullable=True),
    sa.Column('eye_color', mysql.VARCHAR(length=30), nullable=True),
    sa.Column('birth_year', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('gender', mysql.VARCHAR(length=30), nullable=True),
    sa.Column('created', mysql.VARCHAR(length=30), nullable=True),
    sa.Column('edited', mysql.VARCHAR(length=30), nullable=True),
    sa.Column('homeworld', mysql.VARCHAR(length=30), nullable=True),
    sa.Column('description', mysql.VARCHAR(length=30), nullable=True),
    sa.Column('url', mysql.VARCHAR(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('characters')
    # ### end Alembic commands ###
