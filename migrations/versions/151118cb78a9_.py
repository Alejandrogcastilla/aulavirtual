"""empty message

Revision ID: 151118cb78a9
Revises: 8ddb0716c766
Create Date: 2021-05-18 15:48:23.361620

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '151118cb78a9'
down_revision = '8ddb0716c766'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('course_id', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'course_id')
    # ### end Alembic commands ###
