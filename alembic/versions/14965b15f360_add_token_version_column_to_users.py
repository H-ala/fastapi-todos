"""add token_version column to users

Revision ID: 14965b15f360
Revises: 712b03a1cde1
Create Date: 2025-09-05 09:13:01.054318

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14965b15f360'
down_revision: Union[str, Sequence[str], None] = '712b03a1cde1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TABLE users ADD COLUMN token_version INT DEFAULT 0;")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER TABLE users DROP COLUMN token_version;")
