"""Initial Migration

Revision ID: a3001fce1f9e
Revises: 11f91df090b3
Create Date: 2024-11-04 22:02:35.466527

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = "a3001fce1f9e"
down_revision: Union[str, None] = "11f91df090b3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "image",
        sa.Column("id", mysql.CHAR(length=36), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("user_id", mysql.CHAR(length=46), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("image")
    # ### end Alembic commands ###
