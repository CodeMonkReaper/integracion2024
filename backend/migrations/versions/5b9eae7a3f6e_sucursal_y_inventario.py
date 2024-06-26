"""sucursal y inventario 

Revision ID: 5b9eae7a3f6e
Revises: 5bbf83bb1c3d
Create Date: 2024-05-25 13:32:54.940900

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b9eae7a3f6e'
down_revision = '5bbf83bb1c3d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cliente', schema=None) as batch_op:
        batch_op.alter_column('id_cliente',
               existing_type=sa.INTEGER(),
               server_default=None,
               existing_nullable=False,
               autoincrement=True)

    with op.batch_alter_table('producto', schema=None) as batch_op:
        batch_op.add_column(sa.Column('categoria', sa.String(length=100), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('producto', schema=None) as batch_op:
        batch_op.drop_column('categoria')

    with op.batch_alter_table('cliente', schema=None) as batch_op:
        batch_op.alter_column('id_cliente',
               existing_type=sa.INTEGER(),
               server_default=sa.Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1),
               existing_nullable=False,
               autoincrement=True)

    # ### end Alembic commands ###
