"""create user status model

Revision ID: bcbc0978420d
Revises: 7283b03fec2f
Create Date: 2024-10-29 11:12:34.850800

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bcbc0978420d'
down_revision: Union[str, None] = '7283b03fec2f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_status_models',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status_name', sa.String(), nullable=False),
    sa.Column('status_code', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_status_models')
    # ### end Alembic commands ###