"""add knowledge_base table

Revision ID: 002
Revises: 001
Create Date: 2025-10-22

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create knowledge_base table
    op.create_table(
        'knowledge_base',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('source', sa.String(length=500), nullable=True),
        sa.Column('embedding_id', sa.String(length=100), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_knowledge_base_embedding_id'), 'knowledge_base', ['embedding_id'], unique=True)
    op.create_index(op.f('ix_knowledge_base_id'), 'knowledge_base', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_knowledge_base_id'), table_name='knowledge_base')
    op.drop_index(op.f('ix_knowledge_base_embedding_id'), table_name='knowledge_base')
    op.drop_table('knowledge_base')

