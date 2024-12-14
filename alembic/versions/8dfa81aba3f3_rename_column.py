"""rename column

Revision ID: 8dfa81aba3f3
Revises: fcec675136a0
Create Date: 2024-12-13 12:36:59.346707

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8dfa81aba3f3'
down_revision: Union[str, None] = 'fcec675136a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('author', sa.Column('updated_at', sa.Date(), nullable=True))
    op.drop_column('author', 'updeted_at')
    op.add_column('books', sa.Column('updated_at', sa.Date(), nullable=True))
    op.drop_column('books', 'updeted_at')
    op.add_column('readers', sa.Column('updated_at', sa.Date(), nullable=True))
    op.drop_column('readers', 'updeted_at')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('readers', sa.Column('updeted_at', sa.DATE(), autoincrement=False, nullable=True))
    op.drop_column('readers', 'updated_at')
    op.add_column('books', sa.Column('updeted_at', sa.DATE(), autoincrement=False, nullable=True))
    op.drop_column('books', 'updated_at')
    op.add_column('author', sa.Column('updeted_at', sa.DATE(), autoincrement=False, nullable=True))
    op.drop_column('author', 'updated_at')
    # ### end Alembic commands ###
