"""change column in materialcode model from material_name to material_description

Revision ID: 41cf34604be1
Revises: 079f6cea193f
Create Date: 2024-11-07 23:00:22.217948

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '41cf34604be1'
down_revision: Union[str, None] = '079f6cea193f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('material_codes', sa.Column('material_description', sa.String(), nullable=True))
    # op.execute('update material_codes set material_description=material_name')
    op.drop_column('material_codes', 'material_name')
    op.alter_column('users', 'user_status_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'user_status_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.add_column('material_codes', sa.Column('material_name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('material_codes', 'material_description')
    # ### end Alembic commands ###
