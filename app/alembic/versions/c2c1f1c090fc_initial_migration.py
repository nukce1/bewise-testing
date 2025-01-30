"""Initial migration

Revision ID: c2c1f1c090fc
Revises: 
Create Date: 2025-01-15 23:16:48.446014

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2c1f1c090fc'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Application',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Application_id'), 'Application', ['id'], unique=False)
    op.create_index(op.f('ix_Application_user_name'), 'Application', ['user_name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_Application_user_name'), table_name='Application')
    op.drop_index(op.f('ix_Application_id'), table_name='Application')
    op.drop_table('Application')
    # ### end Alembic commands ###
