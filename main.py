import uvicorn
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Body

app = FastAPI()


# Models
class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None


@app.get("/")
def home():
    return {"hello": "world"}


@app.post("/person/new")
def create_person(person: Person = Body(...)):
    # request body. Body makes the parameter needed
    return person


@app.get("/tweets/{tweet_id}")
def get_tweet(tweet_id):
    return {tweet_id: "Some value"}


@app.post("/users/{user_id}/details?age=30&height=184")
def get_user():
    return {}


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info")
