"""add structure id to location model

Revision ID: 3974dfade8f7
Revises: 99ec6a5fa861
Create Date: 2019-03-07 18:44:57.951423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3974dfade8f7'
down_revision = '99ec6a5fa861'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('locations', sa.Column('structure_id', sa.Integer(), nullable=False))
    op.create_foreign_key('locations_structure_id_fkey', 'locations', 'structure', ['structure_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('locations_structure_id_fkey', 'locations', type_='foreignkey')
    op.drop_column('locations', 'structure_id')
    # ### end Alembic commands ###
