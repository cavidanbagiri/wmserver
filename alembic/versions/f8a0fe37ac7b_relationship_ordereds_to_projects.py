"""relationship ordereds to projects

Revision ID: f8a0fe37ac7b
Revises: 454dcb080156
Create Date: 2024-10-20 22:13:43.731487

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f8a0fe37ac7b'
down_revision: Union[str, None] = '454dcb080156'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ordereds', sa.Column('project_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'ordereds', 'projects', ['project_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'ordereds', type_='foreignkey')
    op.drop_column('ordereds', 'project_id')
    # ### end Alembic commands ###