"""Create Model CertPass

Revision ID: 2784a12c8208
Revises: e32b336bb7d4
Create Date: 2024-11-20 11:50:49.612071

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2784a12c8208'
down_revision: Union[str, None] = 'e32b336bb7d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('certpass_models',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('link', sa.String(), nullable=False),
    sa.Column('warehouse_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['warehouse_id'], ['warehouse_materials.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('certpass_models')
    # ### end Alembic commands ###