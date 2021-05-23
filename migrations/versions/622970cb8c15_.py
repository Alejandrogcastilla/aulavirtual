"""empty message

Revision ID: 622970cb8c15
Revises: a6fffac6d221
Create Date: 2021-05-22 22:27:30.698007

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '622970cb8c15'
down_revision = 'a6fffac6d221'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('assignment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('descripcion', sa.Text(), nullable=True),
    sa.Column('date_expire', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('assignment')
    # ### end Alembic commands ###
