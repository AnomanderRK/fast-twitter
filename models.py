"""Contains BaseModels models for current API"""
from __future__ import annotations
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from datetime import date
import uuid


class Tweet(BaseModel):
    tweet_id: uuid.UUID | str = Field(...)
    message: str = Field(..., min_length=25, max_length=170)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    by: User = Field(...)

    class Config:
        """Just for testing API. Default values shown in swagger, for example"""
        schema_extra = {
            "example": {
                "tweet_id": "some_test_id",
                "message": "Some message with more that 25 characters",
            }
        }


class UserBase(BaseModel):
    user_id: uuid.UUID | str = Field(...)
    email: EmailStr = Field(...)


class UserLogin(UserBase):
    password: str = Field(..., min_length=8, max_length=50)


class User(BaseModel):
    first_name: str = Field(..., min_length=5, max_length=50)
    last_name: str = Field(..., min_length=5, max_length=50)
    birthday: Optional[date] = Field(default=None)
