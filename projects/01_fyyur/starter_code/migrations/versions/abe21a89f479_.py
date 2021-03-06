"""empty message

Revision ID: abe21a89f479
Revises: 571ff0b262c9
Create Date: 2020-11-13 10:43:08.660785

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abe21a89f479'
down_revision = '571ff0b262c9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('tmpdatetime', sa.DateTime, nullable=True))
    op.execute('UPDATE "Show" SET tmpdatetime = start_time::timestamp;')
    op.drop_column('Show', 'start_time')
    op.alter_column('Show', 'tmpdatetime', nullable=False, new_column_name='start_time')
    # op.alter_column('Show', 'start_time',
    #            existing_type=sa.VARCHAR(),
    #            type_=sa.DateTime(),
    #            existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Show', 'start_time',
               existing_type=sa.DateTime(),
               type_=sa.VARCHAR(),
               existing_nullable=False)
    # ### end Alembic commands ###
