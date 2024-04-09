"""Create postgres triagram search extension on title

Revision ID: b6d07cded726
Revises: ac4fcc41e102
Create Date: 2024-04-08 16:58:36.808282

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b6d07cded726"
down_revision: Union[str, None] = "ac4fcc41e102"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION pg_trgm;")
    pass


def downgrade() -> None:
    op.execute("DROP EXTENSION IF EXISTS pg_trgm;")
