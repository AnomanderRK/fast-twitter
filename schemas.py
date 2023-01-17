"""Contains BaseModels models for current API"""
from __future__ import annotations
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Any
from datetime import datetime
from datetime import date
import uuid


class UserBase(BaseModel):
    email: EmailStr = Field(...)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=50)
    first_name: str = Field(..., min_length=5, max_length=50)
    last_name: str = Field(..., min_length=5, max_length=50)


class User(UserBase):
    id: int
    birthday: Optional[date] = Field(default=None)
    tweets: List[Any] = []
    # Using list[Tweet] leads to error
    # similar to: https://github.com/pydantic/pydantic/issues/545#issuecomment-496247768

    class Config:
        orm_mode = True


class Tweet(BaseModel):
    id: uuid.UUID = Field(...)
    message: str = Field(..., min_length=25, max_length=170)
    by: User = Field(...)
    user_id: int = Field(...)   # Delete field?
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True
