"""add column project id to areamodel

Revision ID: 1a49b34b1c15
Revises: 8c1cf11ed735
Create Date: 2024-12-11 13:51:06.911899

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a49b34b1c15'
down_revision: Union[str, None] = '8c1cf11ed735'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('areas', sa.Column('project_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'areas', 'projects', ['project_id'], ['id'],)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'areas', type_='foreignkey')
    op.drop_column('areas', 'project_id')
    # ### end Alembic commands ###
