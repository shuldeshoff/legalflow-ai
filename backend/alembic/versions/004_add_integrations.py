"""add integrations and payments

Revision ID: 004
Revises: 003
Create Date: 2025-10-22

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create integrations table
    op.create_table(
        'integrations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('config', sa.JSON(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_integrations_id'), 'integrations', ['id'], unique=False)
    
    # Create integration_logs table
    op.create_table(
        'integration_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('integration_id', sa.Integer(), nullable=False),
        sa.Column('event_type', sa.String(length=100), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('request_data', sa.JSON(), nullable=True),
        sa.Column('response_data', sa.JSON(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['integration_id'], ['integrations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_integration_logs_id'), 'integration_logs', ['id'], unique=False)
    
    # Create telegram_chats table
    op.create_table(
        'telegram_chats',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('chat_id', sa.String(length=100), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('username', sa.String(length=100), nullable=True),
        sa.Column('first_name', sa.String(length=100), nullable=True),
        sa.Column('last_name', sa.String(length=100), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('last_message_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_telegram_chats_id'), 'telegram_chats', ['id'], unique=False)
    op.create_index(op.f('ix_telegram_chats_chat_id'), 'telegram_chats', ['chat_id'], unique=True)
    
    # Create payments table
    op.create_table(
        'payments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('client_id', sa.Integer(), nullable=True),
        sa.Column('amount', sa.Integer(), nullable=False),
        sa.Column('currency', sa.String(length=10), default='RUB'),
        sa.Column('status', sa.String(length=50), default='pending'),
        sa.Column('payment_system', sa.String(length=50), nullable=True),
        sa.Column('payment_id', sa.String(length=200), nullable=True),
        sa.Column('payment_url', sa.String(length=500), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_payments_id'), 'payments', ['id'], unique=False)
    op.create_index(op.f('ix_payments_payment_id'), 'payments', ['payment_id'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_payments_payment_id'), table_name='payments')
    op.drop_index(op.f('ix_payments_id'), table_name='payments')
    op.drop_table('payments')
    
    op.drop_index(op.f('ix_telegram_chats_chat_id'), table_name='telegram_chats')
    op.drop_index(op.f('ix_telegram_chats_id'), table_name='telegram_chats')
    op.drop_table('telegram_chats')
    
    op.drop_index(op.f('ix_integration_logs_id'), table_name='integration_logs')
    op.drop_table('integration_logs')
    
    op.drop_index(op.f('ix_integrations_id'), table_name='integrations')
    op.drop_table('integrations')

