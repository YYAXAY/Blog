"""empty message

Revision ID: 3255b1679c16
Revises: 8bea15b458bc
Create Date: 2020-03-14 12:19:00.104250

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3255b1679c16'
down_revision = '8bea15b458bc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('icon', sa.String(length=64), nullable=True))
    op.alter_column('users', 'confirmed',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=True)
    op.alter_column('users', 'email',
               existing_type=mysql.VARCHAR(charset='utf8', collation='utf8_general_ci', length=64),
               nullable=True)
    op.alter_column('users', 'password_hash',
               existing_type=mysql.VARCHAR(charset='utf8', collation='utf8_general_ci', length=128),
               nullable=True)
    op.alter_column('users', 'username',
               existing_type=mysql.VARCHAR(charset='utf8', collation='utf8_general_ci', length=32),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'username',
               existing_type=mysql.VARCHAR(charset='utf8', collation='utf8_general_ci', length=32),
               nullable=False)
    op.alter_column('users', 'password_hash',
               existing_type=mysql.VARCHAR(charset='utf8', collation='utf8_general_ci', length=128),
               nullable=False)
    op.alter_column('users', 'email',
               existing_type=mysql.VARCHAR(charset='utf8', collation='utf8_general_ci', length=64),
               nullable=False)
    op.alter_column('users', 'confirmed',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=False)
    op.drop_column('users', 'icon')
    # ### end Alembic commands ###
