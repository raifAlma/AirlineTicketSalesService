from alembic import op
import sqlalchemy as sa

revision = '0004'
down_revision = '0003'  # замени на последнюю ревизию, если другая

def upgrade():
    # Добавляем колонки в таблицу aircraft
    op.add_column('aircraft', sa.Column('rows', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('aircraft', sa.Column('seats_per_row', sa.Integer(), nullable=False, server_default='6'))
    op.add_column('aircraft', sa.Column('business_rows', sa.Integer(), nullable=False, server_default='0'))

def downgrade():
    op.drop_column('aircraft', 'rows')
    op.drop_column('aircraft', 'seats_per_row')
    op.drop_column('aircraft', 'business_rows')