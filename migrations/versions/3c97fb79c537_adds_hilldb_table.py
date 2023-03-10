"""adds hilldb table

Revision ID: 3c97fb79c537
Revises: 
Create Date: 2023-01-24 16:34:14.476364

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c97fb79c537'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hilldb',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('analysis', sa.Integer(), nullable=True),
    sa.Column('signals', sa.Integer(), nullable=True),
    sa.Column('screenshot', sa.Integer(), nullable=True),
    sa.Column('help', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('hilldb')
    # ### end Alembic commands ###
