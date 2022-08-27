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
- GET /users/                 Show all users
- GET /users/{user_id}        Get specific user
- PUT /users/{user_id}        Update specific user
- DELETE /users/{user_id}     Delete specific user

"""
from __future__ import annotations
import uuid

from fastapi import FastAPI
from fastapi import Path, Body, status
from fastapi.exceptions import HTTPException
from models import Tweet
from uuid import uuid4

app = FastAPI()


# TODO: get information from database
TEST_TWEETS = [Tweet(tweet_id=uuid4(), message="Some message ............"),
               Tweet(tweet_id=uuid4(), message="Some other message......."),
               Tweet(tweet_id="some_id", message="Some other message 2......."),]


@app.get("/tweets", status_code=status.HTTP_200_OK)
def get_tweets():
    """Show all tweets information"""
    return {tweet.tweet_id: tweet for tweet in TEST_TWEETS}


@app.get("/tweets/{tweet_id}", status_code=status.HTTP_200_OK, response_model=Tweet)
def get_tweet(tweet_id: uuid.UUID | str = Path(..., min_length=5)):
    """Get tween with tweet id"""
    if tweet_id not in [tweet.tweet_id for tweet in TEST_TWEETS]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{tweet_id} not present in data base")
    return list(filter(lambda tweet: tweet.tweet_id == tweet_id, TEST_TWEETS))[0]


@app.post("/tweets/", status_code=status.HTTP_200_OK, response_model=Tweet)
def create_tweet(tweet: Tweet = Body(...)):
    """Create new tweet"""
    TEST_TWEETS.append(tweet)
    return tweet


@app.put("/tweets/{tweet_id}", status_code=status.HTTP_200_OK, response_model=Tweet)
def update_tweet(tweet_id: uuid.UUID | str = Path(...),
                 message: str = Body(...)):
    """Update tweet"""
    if tweet_id not in [tweet.tweet_id for tweet in TEST_TWEETS]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{tweet_id} not found!")

    tweet = list(filter(lambda tweet: tweet.tweet_id == tweet_id, TEST_TWEETS))[0]
    tweet.message = message
    return tweet


@app.delete("/tweets/{tweet_id}", status_code=status.HTTP_200_OK, response_model=Tweet)
def delete_tweet(tweet_id: uuid.UUID | str = Path(...)):
    """Update tweet"""
    if tweet_id not in [tweet.tweet_id for tweet in TEST_TWEETS]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{tweet_id} not found!")

    tweet = list(filter(lambda tweet: tweet.tweet_id == tweet_id, TEST_TWEETS))[0]
    TEST_TWEETS.remove(tweet)
    return tweet
