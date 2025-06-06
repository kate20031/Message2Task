"""Add confirmed field to Message

Revision ID: 9a154457d5f1
Revises: 39e799ad5585
Create Date: 2025-05-30 12:46:08.117729

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a154457d5f1'
down_revision = '39e799ad5585'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.add_column(sa.Column('confirmed', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.drop_column('confirmed')

    # ### end Alembic commands ###
