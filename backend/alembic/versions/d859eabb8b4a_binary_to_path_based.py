"""binary to path based

Revision ID: d859eabb8b4a
Revises: 640c9b56802d
Create Date: 2025-01-11 11:42:55.038547

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd859eabb8b4a'
down_revision: Union[str, None] = '640c9b56802d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
