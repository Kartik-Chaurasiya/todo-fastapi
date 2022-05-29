"""“create-todo”

Revision ID: 7357289e15ed
Revises: 8b623d07ae3e
Create Date: 2022-05-15 11:19:54.320217

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7357289e15ed'
down_revision = '8b623d07ae3e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('todos',
                    sa.Column('todo_id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('todo_text', sa.String(), nullable=False),
                    sa.Column('todo_description', sa.String(), nullable=True),
                    sa.Column('todo_complete_by', sa.Date(), nullable=False),
                    sa.Column('completed', sa.Boolean(), server_default=sa.sql.False_()),
                    sa.Column('is_active', sa.Boolean(), server_default=sa.sql.True_()),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('todo_id'),
                    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
                    )
    pass


def downgrade():
    op.drop_table('todos')
    pass

