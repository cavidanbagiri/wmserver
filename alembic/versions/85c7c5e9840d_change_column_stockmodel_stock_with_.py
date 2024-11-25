"""Change Column StockModel Stock With Leftover

Revision ID: 85c7c5e9840d
Revises: 41cf34604be1
Create Date: 2024-11-13 15:15:12.695841

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '85c7c5e9840d'
down_revision: Union[str, None] = '41cf34604be1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('material_codes', 'material_description',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.add_column('stocks', sa.Column('leftover', sa.Float(), nullable=False))
    op.drop_column('stocks', 'stock')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stocks', sa.Column('stock', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.drop_column('stocks', 'leftover')
    op.alter_column('material_codes', 'material_description',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###