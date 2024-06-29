import uuid
from datetime import datetime
from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from .models import Author, Post, Comment
from .database import get_db
from .schemas import AuthorCreate, PostCreate, CommentCreate, PostPaginationResponse, Post as PostSchema, \
    Comment as CommentSchema, CommentPaginationResponse


class AuthorRepository:

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get(self, author_id: uuid.UUID):
        result = await self.db.execute(select(Author).where(Author.id == author_id))
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 10):
        stmt = select(Author)

        result = await self.db.execute(stmt.offset(skip).limit(limit))
        authors = result.scalars().all()

        return authors

    async def create(self, author: AuthorCreate):
        db_author = Author(id=uuid.uuid4(), name=author.name, email=author.email)
        self.db.add(db_author)
        await self.db.commit()
        await self.db.refresh(db_author)
        return db_author


class PostRepository:

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get(self, post_id: uuid.UUID):
        result = await self.db.execute(select(Post).where(Post.id == post_id).options(joinedload(Post.author), joinedload(Post.comments)))
        return result.scalars().first()

    async def get_all(self, page: int = 1, page_size: int = 10) -> PostPaginationResponse:
        offset = (page - 1) * page_size
        query = select(Post).order_by(Post.id).offset(offset).limit(page_size + 1)
        result = await self.db.execute(query)
        posts = result.scalars().all()

        has_next = len(posts) > page_size
        if has_next:
            posts = posts[:-1]

        has_prev = page > 1

        # Convert ORM models to Pydantic models
        posts_pydantic = [PostSchema.from_orm(post) for post in posts]

        return PostPaginationResponse(data=posts_pydantic, page=page, page_size=page_size, has_next=has_next,
                                      has_prev=has_prev)

    async def create(self, post: PostCreate, author_id: uuid.UUID):
        db_post = Post(id=uuid.uuid4(), title=post.title, content=post.content, author_id=author_id)
        self.db.add(db_post)
        await self.db.commit()
        await self.db.refresh(db_post)
        return db_post


class CommentRepository:

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get(self, comment_id: uuid.UUID):
        result = await self.db.execute(select(Comment).where(Comment.id == comment_id).options(joinedload(Comment.post)))
        return result.scalars().first()

    async def get_all(self, limit: int = 10, cursor: Optional[datetime] = None, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> CommentPaginationResponse:
        query = select(Comment).order_by(Comment.created_at).limit(limit + 1)
        if cursor:
            query = query.where(Comment.created_at > cursor)
        if start_date:
            query = query.where(Comment.created_at >= start_date)
        if end_date:
            query = query.where(Comment.created_at <= end_date)

        result = await self.db.execute(query)
        comments = result.scalars().all()

        has_next = len(comments) > limit
        if has_next:
            comments = comments[:-1]

        # Convert ORM models to Pydantic models
        comments_pydantic = [CommentSchema.from_orm(comment) for comment in comments]

        return CommentPaginationResponse(data=comments_pydantic, limit=limit, has_next=has_next, cursor=comments[-1].created_at if has_next else None)


    async def create(self, comment: CommentCreate, post_id: uuid.UUID):
        db_comment = Comment(id=uuid.uuid4(), content=comment.content, post_id=post_id)
        self.db.add(db_comment)
        await self.db.commit()
        await self.db.refresh(db_comment)
        return db_comment
