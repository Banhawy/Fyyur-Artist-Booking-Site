"""empty message

Revision ID: dcf0ccce1b70
Revises: 7993b6bb5373
Create Date: 2020-10-18 16:08:25.136000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dcf0ccce1b70'
down_revision = '7993b6bb5373'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venue', sa.Column('website', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venue', 'website')
    # ### end Alembic commands ###