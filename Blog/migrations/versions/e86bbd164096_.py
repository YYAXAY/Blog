"""empty message

Revision ID: e86bbd164096
Revises: b776477cbd84
Create Date: 2020-03-14 11:23:19.420542

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e86bbd164096'
down_revision = 'b776477cbd84'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('icon', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'icon')
    # ### end Alembic commands ###
