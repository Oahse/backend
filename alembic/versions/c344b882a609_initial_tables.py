"""Initial tables

Revision ID: c344b882a609
Revises: 
Create Date: 2025-03-09 21:29:46.286873

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c344b882a609'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('firstname', sa.String(length=255), nullable=False),
    sa.Column('lastname', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('role', sa.Enum('Buyer', 'Seller', 'Admin', 'GodAdmin', 'SuperAdmin', 'Moderator', 'Support', 'Manager', name='userrole'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('totalorders', sa.Integer(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('phone_number', sa.String(length=255), nullable=True),
    sa.Column('phone_number_pre', sa.String(length=255), nullable=True),
    sa.Column('tags', sa.String(length=255), nullable=True),
    sa.Column('notes', sa.String(length=255), nullable=True),
    sa.Column('access_token', sa.String(length=255), nullable=False),
    sa.Column('refresh_token', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table('address',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('email_address', sa.String(length=255), nullable=True),
    sa.Column('user_id', sa.String(length=36), nullable=False),
    sa.Column('street', sa.String(length=255), nullable=True),
    sa.Column('city', sa.String(length=255), nullable=True),
    sa.Column('state', sa.String(length=255), nullable=True),
    sa.Column('country', sa.String(length=255), nullable=True),
    sa.Column('post_code', sa.String(length=255), nullable=True),
    sa.Column('kind', sa.Enum('Billing', 'Shipping', name='addresstype'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('address')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
