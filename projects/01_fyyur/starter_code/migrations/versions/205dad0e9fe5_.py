"""empty message

Revision ID: 205dad0e9fe5
Revises: abe21a89f479
Create Date: 2020-11-21 19:59:05.253994

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '205dad0e9fe5'
down_revision = 'abe21a89f479'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ArtistAvailability',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('end_time', sa.DateTime(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('Show', sa.Column('end_time', sa.DateTime(), nullable=True))
    op.execute('UPDATE "Show" SET end_time = start_time + \'4 hour\' where end_time is NULL;')
    op.alter_column('Show', 'end_time', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Show', 'end_time')
    op.drop_table('ArtistAvailability')
    # ### end Alembic commands ###