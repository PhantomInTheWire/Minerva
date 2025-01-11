"""add file_path column to pdfdocument table

Revision ID: a1366f80ea44
Revises: d859eabb8b4a
Create Date: 2025-01-11 11:46:53.857488

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1366f80ea44'
down_revision: Union[str, None] = 'd859eabb8b4a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('pdfdocument', sa.Column('file_path', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('pdfdocument', 'file_path')

