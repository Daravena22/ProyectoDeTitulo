"""empty message

Revision ID: 3097e3b8de34
Revises: 8fd145322815
Create Date: 2023-10-17 21:32:02.095796

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3097e3b8de34'
down_revision = '8fd145322815'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('folios', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rango_desde', sa.String(length=15), nullable=True))
        batch_op.add_column(sa.Column('rango_hasta', sa.String(length=15), nullable=True))
        batch_op.add_column(sa.Column('fecha_vencimiento', sa.Date(), nullable=True))
        batch_op.add_column(sa.Column('rsapk', sa.String(length=1000), nullable=True))
        batch_op.add_column(sa.Column('frma', sa.String(length=1000), nullable=True))
        batch_op.add_column(sa.Column('rsask', sa.String(length=1000), nullable=True))
        batch_op.add_column(sa.Column('rsapubk', sa.String(length=1000), nullable=True))
        batch_op.add_column(sa.Column('ultimo_utilizado', sa.String(length=15), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('folios', schema=None) as batch_op:
        batch_op.drop_column('ultimo_utilizado')
        batch_op.drop_column('rsapubk')
        batch_op.drop_column('rsask')
        batch_op.drop_column('frma')
        batch_op.drop_column('rsapk')
        batch_op.drop_column('fecha_vencimiento')
        batch_op.drop_column('rango_hasta')
        batch_op.drop_column('rango_desde')

    # ### end Alembic commands ###