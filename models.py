"""Contains BaseModels models for current API"""

from pydantic import BaseModel, Field
from uuid import uuid4


class Tweet(BaseModel):
    id: uuid4 = Field(...)
    message: str = Field(..., min_length=25, max_length=170)


class User(BaseModel):
    id: uuid4 = Field(...)
    name: str = Field(..., min_length=5, max_length=50)
