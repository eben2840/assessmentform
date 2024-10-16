"""empty message

Revision ID: c3b43a514f4e
Revises: 3b59dfcb5329
Create Date: 2024-10-10 10:01:47.348405

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3b43a514f4e'
down_revision = '3b59dfcb5329'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('person', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('check_in_time', sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column('check_out_time', sa.DateTime(), nullable=True))
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('person', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('check_out_time')
        batch_op.drop_column('check_in_time')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
