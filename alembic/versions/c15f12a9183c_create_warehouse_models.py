"""create warehouse models

Revision ID: c15f12a9183c
Revises: f31d983c9f04
Create Date: 2024-10-24 04:51:56.232838

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c15f12a9183c'
down_revision: Union[str, None] = 'f31d983c9f04'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('warehouse_materials',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('document', sa.String(), nullable=True),
    sa.Column('material_name', sa.String(), nullable=False),
    sa.Column('quantity', sa.Float(), nullable=False),
    sa.Column('leftover', sa.Float(), nullable=False),
    sa.Column('unit', sa.String(), nullable=False),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('currency', sa.String(), nullable=True),
    sa.Column('po', sa.String(), nullable=True),
    sa.Column('certificate', sa.Boolean(), nullable=False),
    sa.Column('passport', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('created_by_id', sa.Integer(), nullable=False),
    sa.Column('ordered_id', sa.Integer(), nullable=False),
    sa.Column('material_code_id', sa.Integer(), nullable=False),
    sa.Column('material_type_id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.ForeignKeyConstraint(['created_by_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['material_code_id'], ['material_codes.id'], ),
    sa.ForeignKeyConstraint(['material_type_id'], ['material_types.id'], ),
    sa.ForeignKeyConstraint(['ordered_id'], ['ordereds.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('warehouse_materials')
    # ### end Alembic commands ###
