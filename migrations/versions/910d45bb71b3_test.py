"""test

Revision ID: 910d45bb71b3
Revises: 5a210e04c2da
Create Date: 2018-08-28 17:44:13.518977

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '910d45bb71b3'
down_revision = '5a210e04c2da'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('test',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=True),
    sa.Column('location', sa.String(length=200), nullable=True),
    sa.Column('department', sa.String(length=200), nullable=True),
    sa.Column('link', sa.String(length=200), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_test_timestamp'), 'test', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_test_timestamp'), table_name='test')
    op.drop_table('test')
    # ### end Alembic commands ###
