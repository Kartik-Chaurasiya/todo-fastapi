"""“create-user”

Revision ID: 8b623d07ae3e
Revises: 
Create Date: 2022-05-15 10:24:43.620823

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b623d07ae3e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('user_name', sa.String(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('is_active', sa.Boolean(), default=True),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('user_id'),
                    sa.UniqueConstraint('user_name'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
