"""create task_status enum

Revision ID: 599a25ffca0a
Revises: 9ac549eeacd8
Create Date: 2025-12-22 14:40:11.486082

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '599a25ffca0a'
down_revision: Union[str, Sequence[str], None] = '9ac549eeacd8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    task_status_enum = postgresql.ENUM(
        "NEW",
        "IN_PROGRESS",
        "DONE",
        name="task_status",
    )
    task_status_enum.create(op.get_bind(), checkfirst=True)

    op.alter_column(
        "tasks",
        "status",
        existing_type=sa.String(),
        type_=task_status_enum,
        existing_nullable=False,
        postgresql_using="status::task_status" 
    )


def downgrade():
    op.alter_column(
        "tasks",
        "status",
        existing_type=postgresql.ENUM(
            "NEW",
            "IN_PROGRESS",
            "DONE",
            name="task_status",
        ),
        type_=sa.String(),
        existing_nullable=False,
        postgresql_using="status::text"
    )

    task_status_enum = postgresql.ENUM(
        "NEW",
        "IN_PROGRESS",
        "DONE",
        name="task_status",
    )
    task_status_enum.drop(op.get_bind(), checkfirst=True)
