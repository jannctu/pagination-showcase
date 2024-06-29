from datetime import datetime

from fastapi import Depends, HTTPException
from typing import List, Optional
import uuid

from .schemas import Author, AuthorCreate, Post, PostCreate, Comment, CommentCreate, PostPaginationResponse, \
    CommentPaginationResponse
from .repositories import AuthorRepository, PostRepository, CommentRepository


class AuthorCRUD:
    def __init__(self, author_repository: AuthorRepository = Depends()):
        self.author_repository = author_repository

    async def get_author(self, author_id: uuid.UUID) -> Author:
        author = await self.author_repository.get(author_id)
        # debug author
        print(author)
        if author is None:
            raise HTTPException(status_code=404, detail="Author not found")
        return author

    async def get_authors(self, skip: int = 0, limit: int = 10) -> List[Author]:
        return await self.author_repository.get_all(skip=skip, limit=limit)

    async def create_author(self, author: AuthorCreate) -> Author:
        return await self.author_repository.create(author)


class PostCRUD:
    def __init__(self, post_repository: PostRepository = Depends()):
        self.post_repository = post_repository

    async def get_post(self, post_id: uuid.UUID) -> Post:
        post = await self.post_repository.get(post_id)
        if post is None:
            raise HTTPException(status_code=404, detail="Post not found")
        return post

    async def get_posts(self, page: int = 1, page_size: int = 10) -> PostPaginationResponse:
        result = await self.post_repository.get_all(page=page, page_size=page_size)

        return result

    async def create_post(self, post: PostCreate, author_id: uuid.UUID) -> Post:
        return await self.post_repository.create(post, author_id)


class CommentCRUD:
    def __init__(self, comment_repository: CommentRepository = Depends()):
        self.comment_repository = comment_repository

    async def get_comment(self, comment_id: uuid.UUID) -> Comment:
        comment = await self.comment_repository.get(comment_id)
        if comment is None:
            raise HTTPException(status_code=404, detail="Comment not found")
        return comment

    async def get_comments(self, limit: int = 10, cursor: Optional[datetime] = None, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> CommentPaginationResponse:
        return await self.comment_repository.get_all(limit=limit, cursor=cursor, start_date=start_date, end_date=end_date)

    async def create_comment(self, comment: CommentCreate, post_id: uuid.UUID) -> Comment:
        return await self.comment_repository.create(comment, post_id)
