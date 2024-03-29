"""empty message

Revision ID: 4db85724c676
Revises: e40311c48709
Create Date: 2023-11-13 23:35:07.995856

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4db85724c676'
down_revision = 'e40311c48709'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('categoria', schema=None) as batch_op:
        batch_op.add_column(sa.Column('estado', sa.Double(), nullable=True))

    with op.batch_alter_table('cliente', schema=None) as batch_op:
        batch_op.add_column(sa.Column('estado', sa.Double(), nullable=True))

    with op.batch_alter_table('material', schema=None) as batch_op:
        batch_op.add_column(sa.Column('estado', sa.Double(), nullable=True))

    with op.batch_alter_table('producto', schema=None) as batch_op:
        batch_op.add_column(sa.Column('estado', sa.Double(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('producto', schema=None) as batch_op:
        batch_op.drop_column('estado')

    with op.batch_alter_table('material', schema=None) as batch_op:
        batch_op.drop_column('estado')

    with op.batch_alter_table('cliente', schema=None) as batch_op:
        batch_op.drop_column('estado')

    with op.batch_alter_table('categoria', schema=None) as batch_op:
        batch_op.drop_column('estado')

    # ### end Alembic commands ###
