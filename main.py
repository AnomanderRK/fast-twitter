from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"hello": "world"}


@app.get("/tweets/{tweet_id}")
def get_tweet(tweet_id):
    return {tweet_id: "Some value"}


@app.post("/users/{user_id}/details?age=30&height=184")
def get_user():
    return {}


if __name__ == "__main__":
    pass