"""Contains BaseModels models for current API"""
from __future__ import annotations
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from datetime import date
import uuid


class UserBase(BaseModel):
    user_id: uuid.UUID = Field(...)
    email: EmailStr = Field(...)


class UserLogin(UserBase):
    password: str = Field(..., min_length=8, max_length=50)


class User(UserBase):
    first_name: str = Field(..., min_length=5, max_length=50)
    last_name: str = Field(..., min_length=5, max_length=50)
    birthday: Optional[date] = Field(default=None)


class UserRegister(User, UserLogin):
    ...


class Tweet(BaseModel):
    tweet_id: uuid.UUID = Field(...)
    message: str = Field(..., min_length=25, max_length=170)
    by: User = Field(...)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)