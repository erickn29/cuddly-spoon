"""init

Revision ID: e39081702736
Revises: 
Create Date: 2024-08-23 15:51:53.908342

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e39081702736"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("email", sa.String(length=32), nullable=False),
        sa.Column("password", sa.String(length=512), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_admin", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("user_id", name=op.f("pk_user")),
        sa.UniqueConstraint("email", name=op.f("uq_user_email")),
        sa.UniqueConstraint("user_id", name=op.f("uq_user_user_id")),
    )
    op.create_table(
        "bot",
        sa.Column("bot_id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("phone", sa.String(length=16), nullable=False),
        sa.Column("alias", sa.String(length=16), nullable=True),
        sa.Column("config", sa.JSON(), nullable=False),
        sa.Column("session", sa.JSON(), nullable=False),
        sa.Column("is_stopped", sa.Boolean(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"], ["user.user_id"], name="user_id", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("bot_id", name=op.f("pk_bot")),
        sa.UniqueConstraint("bot_id", name=op.f("uq_bot_bot_id")),
        sa.UniqueConstraint("phone", name=op.f("uq_bot_phone")),
    )
    op.create_table(
        "comment",
        sa.Column("comment_id", sa.UUID(), nullable=False),
        sa.Column("bot_id", sa.UUID(), nullable=False),
        sa.Column("post_url", sa.String(length=512), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["bot_id"], ["bot.bot_id"], name="bot_id", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("comment_id", name=op.f("pk_comment")),
        sa.UniqueConstraint("comment_id", name=op.f("uq_comment_comment_id")),
    )
    op.create_table(
        "task",
        sa.Column("task_id", sa.UUID(), nullable=False),
        sa.Column("bot_id", sa.UUID(), nullable=False),
        sa.Column("is_executed", sa.Boolean(), nullable=False),
        sa.Column("data", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["bot_id"], ["bot.bot_id"], name="bot_id", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("task_id", name=op.f("pk_task")),
        sa.UniqueConstraint("task_id", name=op.f("uq_task_task_id")),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("task")
    op.drop_table("comment")
    op.drop_table("bot")
    op.drop_table("user")
    # ### end Alembic commands ###
