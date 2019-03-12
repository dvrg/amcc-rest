"""remove unique

Revision ID: dbdff5de41c8
Revises: 010e5d191217
Create Date: 2019-03-12 22:31:12.903798

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dbdff5de41c8'
down_revision = '010e5d191217'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'pesawat_kode_key', 'pesawat', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(u'pesawat_kode_key', 'pesawat', ['kode'])
    # ### end Alembic commands ###
