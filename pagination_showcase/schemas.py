from typing import List, Optional

from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime


class AuthorBase(BaseModel):
    name: str
    email: EmailStr


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Enable orm_mode


class PostPaginationResponse(BaseModel):
    data: List[Post]
    page: int
    page_size: int
    has_next: bool
    has_prev: bool


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Enable orm_mode


class CommentPaginationResponse(BaseModel):
    data: List[Comment]
    limit: int
    has_next: bool
    cursor: Optional[datetime]


