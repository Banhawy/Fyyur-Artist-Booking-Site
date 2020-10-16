"""empty message

Revision ID: 60c3e9c3cc54
Revises: dcf4705e4b7e
Create Date: 2020-10-15 06:03:29.346935

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60c3e9c3cc54'
down_revision = 'dcf4705e4b7e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('show',
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], ),
    sa.PrimaryKeyConstraint('artist_id', 'venue_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('show')
    # ### end Alembic commands ###