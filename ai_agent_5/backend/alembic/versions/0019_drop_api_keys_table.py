"""drop api_keys table

Revision ID: 0019_drop_api_keys_table
Revises: 0018_user_slash_commands
Create Date: 2026-05-10T00:00:00+00:00

User-scoped API keys feature was removed (no endpoint ever consumed them as
auth — they only existed for CRUD). Drop the table on existing deployments.
"""

import sqlalchemy as sa

from alembic import op

revision = "0019_drop_api_keys_table"
down_revision = "0018_user_slash_commands"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_table("api_keys")


def downgrade() -> None:
    op.create_table(
        "api_keys",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            sa.dialects.postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("key_hash", sa.String(255), nullable=False, unique=True),
        sa.Column("prefix", sa.String(16), nullable=False),
        sa.Column("last_used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
