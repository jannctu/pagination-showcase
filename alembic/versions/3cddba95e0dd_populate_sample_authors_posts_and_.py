"""Populate sample authors, posts, and comments

Revision ID: 3cddba95e0dd
Revises: 22ff477140d6
Create Date: 2024-06-28 18:09:08.531316

"""
from typing import Sequence, Union

from alembic import op
from datetime import datetime
import  uuid
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3cddba95e0dd'
down_revision: Union[str, None] = '22ff477140d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Generate UUIDs for authors and posts
author1_id = uuid.uuid4()
author2_id = uuid.uuid4()
post1_id = uuid.uuid4()
post2_id = uuid.uuid4()

def upgrade():
    # Insert sample authors
    op.execute("""
    INSERT INTO authors (id, name, email, created_at, updated_at) VALUES
    ('{author1_id}', 'Author One', 'author1@example.com', '{now}', '{now}'),
    ('{author2_id}', 'Author Two', 'author2@example.com', '{now}', '{now}');
    """.format(
        author1_id=author1_id,
        author2_id=author2_id,
        now=datetime.utcnow().isoformat()
    ))

    # Insert sample posts
    op.execute("""
    INSERT INTO posts (id, title, content, author_id, created_at, updated_at) VALUES
    ('{post1_id}', 'Post One', 'Content for post one.', '{author1_id}', '{now}', '{now}'),
    ('{post2_id}', 'Post Two', 'Content for post two.', '{author2_id}', '{now}', '{now}');
    """.format(
        post1_id=post1_id,
        post2_id=post2_id,
        author1_id=author1_id,
        author2_id=author2_id,
        now=datetime.utcnow().isoformat()
    ))

    # Insert sample comments
    op.execute("""
    INSERT INTO comments (id, content, post_id, created_at, updated_at) VALUES
    ('{comment1_id}', 'Comment for post one.', '{post1_id}', '{now}', '{now}'),
    ('{comment2_id}', 'Comment for post two.', '{post2_id}', '{now}', '{now}');
    """.format(
        comment1_id=uuid.uuid4(),
        comment2_id=uuid.uuid4(),
        post1_id=post1_id,
        post2_id=post2_id,
        now=datetime.utcnow().isoformat()
    ))


def downgrade():
    # Delete sample comments
    op.execute("""
    DELETE FROM comments WHERE content IN ('Comment for post one.', 'Comment for post two.');
    """)

    # Delete sample posts
    op.execute("""
    DELETE FROM posts WHERE title IN ('Post One', 'Post Two');
    """)

    # Delete sample authors
    op.execute("""
    DELETE FROM authors WHERE name IN ('Author One', 'Author Two');
    """)