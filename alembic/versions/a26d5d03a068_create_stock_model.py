"""create stock model

Revision ID: a26d5d03a068
Revises: c15f12a9183c
Create Date: 2024-10-25 11:25:26.919350

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a26d5d03a068'
down_revision: Union[str, None] = 'c15f12a9183c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stocks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('qty', sa.Float(), nullable=False),
    sa.Column('stock', sa.Float(), nullable=False),
    sa.Column('serial_number', sa.String(), nullable=False),
    sa.Column('material_id', sa.String(), nullable=False),
    sa.Column('created_by_id', sa.Integer(), nullable=False),
    sa.Column('warehouse_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['created_by_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['warehouse_id'], ['warehouse_materials.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stocks')
    # ### end Alembic commands ###
