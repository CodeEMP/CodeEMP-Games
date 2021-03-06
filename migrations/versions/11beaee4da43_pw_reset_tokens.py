"""pw reset tokens

Revision ID: 11beaee4da43
Revises: a6cb935d2c19
Create Date: 2018-08-21 15:15:38.546360

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11beaee4da43'
down_revision = 'a6cb935d2c19'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('friend', sa.Column('friended_id', sa.Integer(), nullable=True))
    op.add_column('friend', sa.Column('friender_id', sa.Integer(), nullable=True))
    op.drop_constraint(None, 'friend', type_='foreignkey')
    op.create_foreign_key(None, 'friend', 'user', ['friended_id'], ['id'])
    op.create_foreign_key(None, 'friend', 'user', ['friender_id'], ['id'])
    op.drop_column('friend', 'friend_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('friend', sa.Column('friend_id', sa.INTEGER(), nullable=True))
    op.drop_constraint(None, 'friend', type_='foreignkey')
    op.drop_constraint(None, 'friend', type_='foreignkey')
    op.create_foreign_key(None, 'friend', 'user', ['friend_id'], ['id'])
    op.drop_column('friend', 'friender_id')
    op.drop_column('friend', 'friended_id')
    # ### end Alembic commands ###
