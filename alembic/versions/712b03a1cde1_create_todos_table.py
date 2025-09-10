"""create todos table

Revision ID: 712b03a1cde1
Revises: e8dc160daf47
Create Date: 2025-09-04 11:05:28.954817

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '712b03a1cde1'
down_revision: Union[str, Sequence[str], None] = 'e8dc160daf47'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
    """
    CREATE TABLE todos (
        id SERIAL PRIMARY KEY,
        title VARCHAR(50) NOT NULL, 
        description VARCHAR(200),
        priority INTEGER CHECK (priority >= 1 AND priority <=5),
        complete BOOLEAN NOT NULL DEFAULT FALSE,
        owner_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
    """
)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
    "DROP TABLE todos;"
)
