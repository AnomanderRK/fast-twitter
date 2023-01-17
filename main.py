"""
Run server: uvicorn main:app --reload

# End points design
## Tweets
- GET /tweets/                Show all tweets
- GET /tweets/{id}      show specific tweet
- POST /tweets/               Create new tweet
- PUT /tweet/{id}       Update specific tweet
- DELETE /tweet/{id}    Delete specific tweet

## Authentication
- POST /auth/signup           Register new user
- POST /auth/login            Login a user

## Users
- PUT /auth/login             login user
- PUT /auth/signup            sign up new user
- GET /users/                 Show all users
- GET /users/{id}        Get specific user
- PUT /users/{id}        Update specific user
- DELETE /users/{id}     Delete specific user

TODO: https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-sqlalchemy-parts
"""
import uuid
import json

from fastapi import FastAPI, Depends
from fastapi import Path, Body, Form, status
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from pydantic import EmailStr
from schemas import Tweet, User, UserCreate
from uuid import uuid4
from typing import Optional, Any, Protocol, List
from datetime import date
import models
import crud
import schemas
from database import SessionLocal, engine
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Path operations
# Tweets path operations

@app.get(path="/", response_class=RedirectResponse,
         summary="Show all tweets", tags=["Tweets"])
def home():
    """Show all tweets information. Redirect to /tweets"""
    return "/tweets"


@app.get("/tweets", status_code=status.HTTP_200_OK, response_model=List[Tweet],
         summary="Show all tweets", tags=["Tweets"])
def get_tweets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    This path operation shows all tweets in the app

    Returns
    -------
    Json list with all tweets in the app
    """
    tweets = crud.get_tweets(db, skip, limit)
    return tweets


@app.get("/tweets/{id}", response_model=Tweet, status_code=status.HTTP_200_OK,
         response_model_exclude={"created_at"}, summary="Show a tweet", tags=["Tweets"])
def get_tweet(tweet_id: int = Path(...), db: Session = Depends(get_db)):
    """
    Get tween with tweet id

    Returns
    -------
    Tweet information
    """
    db_tweet = crud.get_tweet(db, tweet_id)
    if db_tweet is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Tweet not found")
    return db_tweet


@app.post("/users/{id}/tweets/", response_model=Tweet, status_code=status.HTTP_201_CREATED,
          summary="Post a tweet", tags=["Tweets"])
def post_tweet(user_id: int, tweet: schemas.Tweet = Body(...), db: Session = Depends(get_db)) -> Tweet:
    """
    This Path operation post a tweet

    Parameters
    ----------
    - id: User posting the tweet
    - tweet: Tweet information

    Returns
    -------
    A json with basic tweet information
    """
    return crud.create_user_tweet(db, tweet, user_id=user_id)


# Users path operations
@app.post(path="/users", response_model=schemas.User, status_code=status.HTTP_201_CREATED,
          summary="Register a new user", tags=["Users"])
def register_new_user(user: schemas.UserCreate = Body(...),
                      db: Session = Depends(get_db)):
    """
    This Path operation register a new user

    Parameters
    ----------
    - user: User information of type UserRegister

    Returns
    -------
    A json with basic information for the user
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User already registered")
    return crud.create_user(db, user)


@app.get(path="/users", response_model=list[schemas.User], status_code=status.HTTP_200_OK,
         summary="Show all users", tags=["Users"])
def show_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[User]:
    """
    This path operation shows all users in the app

    Returns
    -------
    Json list with all Users in the app
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

#
# @app.get(path="/users/{id}", response_model=schemas.User, status_code=status.HTTP_200_OK,
#          summary="Get information for specific user", tags=["Users"])
# def show_user(id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, id=id)
#     if db_user is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="User not found!")
#     return db_user
#
