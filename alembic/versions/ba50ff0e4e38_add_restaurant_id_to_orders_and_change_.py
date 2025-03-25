"""Add restaurant_id to orders and change relationships in model

Revision ID: ba50ff0e4e38
Revises: 7b22624af1e1
Create Date: 2025-03-25 17:11:03.366434

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba50ff0e4e38'
down_revision: Union[str, None] = '7b22624af1e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('restaurant_id', sa.UUID(), nullable=False))
    op.add_column('orders', sa.Column('name', sa.String(), nullable=True))
    op.create_foreign_key(None, 'orders', 'restaurants', ['restaurant_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.drop_column('orders', 'name')
    op.drop_column('orders', 'restaurant_id')
    # ### end Alembic commands ###
