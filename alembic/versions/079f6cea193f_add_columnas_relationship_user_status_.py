"""add columnas relationship user_status_models.id to user model

Revision ID: 079f6cea193f
Revises: 85f4ea8c446a
Create Date: 2024-10-29 12:05:45.566368

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '079f6cea193f'
down_revision: Union[str, None] = '85f4ea8c446a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('user_status_id', sa.Integer(), nullable=True))
    op.alter_column('users', 'is_admin',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.create_foreign_key(None, 'users', 'user_status_models', ['user_status_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.alter_column('users', 'is_admin',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.drop_column('users', 'user_status_id')
    # ### end Alembic commands ###