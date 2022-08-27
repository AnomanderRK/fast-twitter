"""Contains BaseModels models for current API"""
from __future__ import annotations
from pydantic import BaseModel, Field
import uuid


class Tweet(BaseModel):
    tweet_id: uuid.UUID | str = Field(...)
    message: str = Field(..., min_length=25, max_length=170)

    class Config:
        """Just for testing API. Default values shown in swagger, for example"""
        schema_extra = {
            "example": {
                "tweet_id": "some_test_id",
                "message": "Some message with more that 25 characters",
            }
        }


class User(BaseModel):
    user_id: uuid.UUID | str = Field(...)
    name: str = Field(..., min_length=5, max_length=50)
