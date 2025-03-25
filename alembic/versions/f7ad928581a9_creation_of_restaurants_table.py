"""Creation of restaurants table

Revision ID: f7ad928581a9
Revises: 3f6e2e47b00e
Create Date: 2025-03-25 15:10:54.695630

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f7ad928581a9'
down_revision: Union[str, None] = '4cda01703f4f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('restaurants',
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('address', sa.String(), nullable=False),
                    sa.Column('city', sa.String(), nullable=False),
                    sa.Column('state', sa.String(), nullable=False),
                    sa.Column('zip_code', sa.String(), nullable=False),
                    sa.Column('description', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('restaurants')
    # ### end Alembic commands ###
