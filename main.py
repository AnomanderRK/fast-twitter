"""
Run server: uvicorn main:app --reload

# End points design
## Tweets
- GET /tweets/                Show all tweets
- GET /tweets/{tweet_id}      show specific tweet
- POST /tweets/               Create new tweet
- PUT /tweet/{tweet_id}       Update specific tweet
- DELETE /tweet/{tweet_id}    Delete specific tweet

## Authentication
- POST /auth/signup           Register new user
- POST /auth/login            Login a user

## Users
- PUT /auth/login             login user
- PUT /auth/signup            sign up new user
- GET /users/                 Show all users
- GET /users/{user_id}        Get specific user
- PUT /users/{user_id}        Update specific user
- DELETE /users/{user_id}     Delete specific user

"""
from __future__ import annotations
import uuid
import json

from fastapi import FastAPI
from fastapi import Path, Body, Form, status
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from pydantic import EmailStr
from models import Tweet, User, UserRegister
from uuid import uuid4
from typing import Optional, Any
from datetime import date


app = FastAPI()


# TODO: get information from database
TEST_TWEETS = [Tweet(tweet_id=uuid4(), message="Some message ............."),
               Tweet(tweet_id=uuid4(), message="Some other message......."),
               Tweet(tweet_id=uuid4(), message="Some other message 2.......")]


def retrieve_tweet(tweet_id: uuid.UUID) -> Optional[Tweet]:
    """Retrieve tweet with tweet id"""
    try:
        tweet = list(filter(lambda tw: tw.tweet_id == tweet_id, TEST_TWEETS))[0]
    except IndexError:
        raise Exception(f"Tweet id: {tweet_id} not present")
    return tweet


# Path operations
# Tweets path operations

@app.get(path="/", response_class=RedirectResponse,
         summary="Show all tweets", tags=["Tweets"])
def home():
    """Show all tweets information. Redirect to /tweets"""
    return "/tweets"


@app.get("/tweets", status_code=status.HTTP_200_OK,
         summary="Show all tweets", tags=["Tweets"])
def get_tweets():
    """Show all tweets information"""
    return {tweet.tweet_id: tweet for tweet in TEST_TWEETS}


# @app.get("/tweets/{tweet_id}", response_model=Tweet, status_code=status.HTTP_200_OK,
#          summary="Show a tweet", tags=["Tweets"])
# def get_tweet(tweet_id: uuid.UUID = Path(..., min_length=5)):
#     """Get tween with tweet id"""
#     if tweet_id not in [tweet.tweet_id for tweet in TEST_TWEETS]:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"{tweet_id} not present in data base")
#     return list(filter(lambda tweet: tweet.tweet_id == tweet_id, TEST_TWEETS))[0]
#
#
# @app.post("/tweets/", response_model=Tweet, status_code=status.HTTP_201_CREATED,
#           summary="Create a tweet", tags=["Tweets"])
# def create_tweet(tweet: Tweet = Body(...)):
#     """Create new tweet"""
#     TEST_TWEETS.append(tweet)
#     return tweet
#
#
# @app.put("/tweets/{tweet_id}", response_model=Tweet, status_code=status.HTTP_201_CREATED,
#          summary="Update a tweet", tags=["Tweets"])
# def update_tweet(tweet_id: uuid.UUID = Path(...),
#                  message: str = Body(...)):
#     """Update tweet"""
#     if tweet_id not in [tweet.tweet_id for tweet in TEST_TWEETS]:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"{tweet_id} not found!")
#
#     tweet = retrieve_tweet(tweet_id)
#     tweet.message = message
#     return tweet
#
#
# @app.delete("/tweets/{tweet_id}", response_model=Tweet, status_code=status.HTTP_200_OK,
#             summary="Delete a tweet", tags=["Tweets"])
# def delete_tweet(tweet_id: uuid.UUID = Path(...)):
#     """Update tweet"""
#     if tweet_id not in [tweet.tweet_id for tweet in TEST_TWEETS]:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"{tweet_id} not found!")
#
#     tweet = retrieve_tweet(tweet_id)
#     TEST_TWEETS.remove(tweet)
#     return tweet


# Users path operations
@app.post(path="/auth/signup", response_model=User, status_code=status.HTTP_201_CREATED,
          summary="Register a new user", tags=["Users"])
def register_new_user(user: UserRegister = Body(...)) -> User:
    """
    This Path operation register a new user

    Parameters
    ----------
    - user: User information of type UserRegister

    Returns
    -------
    A json with basic information for the user
    """
    with open("users.json", "r+", encoding="utf-8") as f:
        results: list[dict[str, str]] = json.load(f)
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birthday"] = str(user_dict["birthday"])
        results.append(user_dict)
        f.seek(0)
        json.dump(results, f)
    return user


@app.post(path="/auth/login", response_model=User, status_code=status.HTTP_200_OK,
          summary="Login user", tags=["Users"])
def login():
    pass


@app.get(path="/users", response_model=list[User], status_code=status.HTTP_200_OK,
         summary="Show all users", tags=["Users"])
def show_all_users():
    pass


@app.get(path="/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK,
         summary="Get information for specific user", tags=["Users"])
def show_user():
    pass


@app.delete(path="/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK,
            summary="Delete a user", tags=["Users"])
def delete_user():
    pass


@app.put(path="/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK,
         summary="Update user", tags=["Users"])
def update_user():
    pass
