from datetime import datetime

from fastapi import APIRouter, Depends
from typing import List, Optional
from uuid import UUID

from .schemas import Author, AuthorCreate, Post, PostCreate, Comment, CommentCreate, PostPaginationResponse, \
    CommentPaginationResponse
from .crud import AuthorCRUD, PostCRUD, CommentCRUD

router = APIRouter()

# Author routes
@router.post("/authors/", response_model=Author)
async def create_author(author: AuthorCreate, author_crud: AuthorCRUD = Depends()):
    return await author_crud.create_author(author)

@router.get("/authors/{author_id}", response_model=Author)
async def read_author(author_id: UUID, author_crud: AuthorCRUD = Depends()):
    return await author_crud.get_author(author_id)

@router.get("/authors/", response_model=List[Author])
async def read_authors(skip: int = 0, limit: int = 10, author_crud: AuthorCRUD = Depends()):
    return await author_crud.get_authors(skip=skip, limit=limit)


# Post routes
@router.post("/posts/", response_model=Post)
async def create_post(post: PostCreate, author_id: UUID, post_crud: PostCRUD = Depends()):
    return await post_crud.create_post(post, author_id)

@router.get("/posts/{post_id}", response_model=Post)
async def read_post(post_id: UUID, post_crud: PostCRUD = Depends()):
    return await post_crud.get_post(post_id)

@router.get("/posts/", response_model=PostPaginationResponse)
async def read_posts(page: int = 1, page_size: int = 10, post_crud: PostCRUD = Depends()):
    return await post_crud.get_posts(page=page, page_size=page_size)


# Comment routes
@router.post("/comments/", response_model=Comment)
async def create_comment(comment: CommentCreate, post_id: UUID, comment_crud: CommentCRUD = Depends()):
    return await comment_crud.create_comment(comment, post_id)

@router.get("/comments/{comment_id}", response_model=Comment)
async def read_comment(comment_id: UUID, comment_crud: CommentCRUD = Depends()):
    return await comment_crud.get_comment(comment_id)

@router.get("/comments/", response_model=CommentPaginationResponse)
async def read_comments(limit: int = 10, cursor: Optional[datetime] = None, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None, comment_crud: CommentCRUD = Depends()):
    return await comment_crud.get_comments(limit=limit, cursor=cursor, start_date=start_date, end_date=end_date)
