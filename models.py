"""Contains BaseModels models for current API"""
from __future__ import annotations
from pydantic import BaseModel, Field
import uuid


class Tweet(BaseModel):
    tweet_id: uuid.UUID | str = Field(...)
    message: str = Field(..., min_length=25, max_length=170)


class User(BaseModel):
    user_id: uuid.UUID | str = Field(...)
    name: str = Field(..., min_length=5, max_length=50)
