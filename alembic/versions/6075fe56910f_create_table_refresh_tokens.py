"""create table refresh_tokens

Revision ID: 6075fe56910f
Revises: 14965b15f360
Create Date: 2025-09-05 09:15:52.885542

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6075fe56910f'
down_revision: Union[str, Sequence[str], None] = '14965b15f360'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE TABLE refresh_token (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            jti VARCHAR(64) NOT NULL UNIQUE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            revoked BOOLEAN NOT NULL DEFAULT FALSE,
            replaced_by VARCHAR(64)
        );
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE refresh_token;")
