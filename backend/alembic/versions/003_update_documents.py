"""update documents table

Revision ID: 003
Revises: 002
Create Date: 2025-10-22

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add new columns to documents table
    op.add_column('documents', sa.Column('file_type', sa.String(length=50), nullable=True))
    op.add_column('documents', sa.Column('file_size', sa.Integer(), nullable=True))
    op.add_column('documents', sa.Column('uploaded_by', sa.Integer(), nullable=True))
    op.add_column('documents', sa.Column('extracted_text', sa.Text(), nullable=True))
    op.add_column('documents', sa.Column('analysis_status', sa.String(length=50), server_default='pending', nullable=True))
    op.add_column('documents', sa.Column('analysis_summary', sa.Text(), nullable=True))
    op.add_column('documents', sa.Column('key_points', sa.JSON(), nullable=True))
    op.add_column('documents', sa.Column('risks', sa.JSON(), nullable=True))
    op.add_column('documents', sa.Column('recommendations', sa.Text(), nullable=True))
    op.add_column('documents', sa.Column('analyzed_at', sa.DateTime(), nullable=True))
    op.add_column('documents', sa.Column('embedding_id', sa.String(length=100), nullable=True))
    
    # Add foreign key for uploaded_by
    op.create_foreign_key('fk_documents_uploaded_by', 'documents', 'users', ['uploaded_by'], ['id'])


def downgrade() -> None:
    # Drop foreign key
    op.drop_constraint('fk_documents_uploaded_by', 'documents', type_='foreignkey')
    
    # Drop columns
    op.drop_column('documents', 'embedding_id')
    op.drop_column('documents', 'analyzed_at')
    op.drop_column('documents', 'recommendations')
    op.drop_column('documents', 'risks')
    op.drop_column('documents', 'key_points')
    op.drop_column('documents', 'analysis_summary')
    op.drop_column('documents', 'analysis_status')
    op.drop_column('documents', 'extracted_text')
    op.drop_column('documents', 'uploaded_by')
    op.drop_column('documents', 'file_size')
    op.drop_column('documents', 'file_type')

