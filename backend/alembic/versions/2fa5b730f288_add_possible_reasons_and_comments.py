from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '2fa5b730f288'
down_revision: Union[str, None] = 'b0f70df93352'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table('comments',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('prediction_id', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('upvotes', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('downvotes', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['prediction_id'], ['predictions.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment_votes',
    sa.Column('comment_id', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('vote_type', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['comment_id'], ['comments.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('comment_id', 'user_id')
    )
    op.add_column('predictions', sa.Column('possible_reasons', sa.Text(), nullable=True))
    op.add_column('predictions', sa.Column('location', sa.String(length=100), nullable=True))
    op.add_column('predictions', sa.Column('language', sa.String(length=50), nullable=True))

def downgrade() -> None:
    op.drop_column('predictions', 'language')
    op.drop_column('predictions', 'location')
    op.drop_column('predictions', 'possible_reasons')
    op.drop_table('comment_votes')
    op.drop_table('comments')
