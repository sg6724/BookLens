from __future__ import annotations

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_init'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'books',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(length=512), nullable=False, index=True),
        sa.Column('author', sa.String(length=512), nullable=False, index=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('google_books_id', sa.String(length=128), nullable=True, unique=True),
        sa.Column('cover_url', sa.String(length=1024), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        'summaries',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('book_id', sa.Integer(), sa.ForeignKey('books.id', ondelete='CASCADE'), index=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tone', sa.String(length=64), nullable=False),
        sa.Column('length', sa.String(length=64), nullable=False),
        sa.Column('audience', sa.String(length=64), nullable=False),
        sa.Column('audio_path', sa.String(length=1024), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        'embeddings',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('book_id', sa.Integer(), sa.ForeignKey('books.id', ondelete='CASCADE'), index=True),
        sa.Column('embedding', sa.LargeBinary(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        'user_library',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('book_id', sa.Integer(), sa.ForeignKey('books.id', ondelete='CASCADE'), index=True),
        sa.Column('is_liked', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint('book_id', name='uq_userlibrary_book'),
    )


def downgrade() -> None:
    op.drop_table('user_library')
    op.drop_table('embeddings')
    op.drop_table('summaries')
    op.drop_table('books')
