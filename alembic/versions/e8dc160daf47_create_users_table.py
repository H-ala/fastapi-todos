"""create users table

Revision ID: e8dc160daf47
Revises: 
Create Date: 2025-09-04 10:41:41.844662

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8dc160daf47'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50), 
            last_name VARCHAR(50),
            username VARCHAR(60) NOT NULL UNIQUE,
            email VARCHAR(200) NOT NULL UNIQUE,
            hashed_password VARCHAR(200) NOT NULL,
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            role VARCHAR(10) NOT NULL DEFAULT 'user',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        "DROP TABLE users;"
    )
