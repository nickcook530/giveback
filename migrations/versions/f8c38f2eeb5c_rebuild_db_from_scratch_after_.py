"""rebuild db from scratch after accidental delete)


Revision ID: f8c38f2eeb5c
Revises: 
Create Date: 2019-10-11 02:26:24.931225

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8c38f2eeb5c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_category_name'), 'category', ['name'], unique=True)
    op.create_index(op.f('ix_category_parent_id'), 'category', ['parent_id'], unique=False)
    op.create_table('company',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('image_url', sa.String(length=128), nullable=True),
    sa.Column('website_url', sa.String(length=218), nullable=True),
    sa.Column('product_description', sa.String(length=300), nullable=True),
    sa.Column('cause_url', sa.String(length=218), nullable=True),
    sa.Column('cause_description', sa.String(length=300), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_company_name'), 'company', ['name'], unique=True)
    op.create_table('tags',
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
    sa.PrimaryKeyConstraint('company_id', 'category_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tags')
    op.drop_index(op.f('ix_company_name'), table_name='company')
    op.drop_table('company')
    op.drop_index(op.f('ix_category_parent_id'), table_name='category')
    op.drop_index(op.f('ix_category_name'), table_name='category')
    op.drop_table('category')
    # ### end Alembic commands ###