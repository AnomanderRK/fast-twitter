import uvicorn
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Body, Query, Path

app = FastAPI()


# Models
class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None


class Location(BaseModel):
    city: str
    state: str
    country: str


@app.get("/")
def home():
    return {"hello": "world"}


@app.post("/person/new")
def create_person(person: Person = Body(...)):
    # request body. Body makes the parameter needed
    return person


@app.get("/person/detail")
def show_person(name: Optional[str] = Query(default=None,
                                            min_length=1,
                                            max_length=50,
                                            title="Person's name",
                                            description="This is the person's name. It is between 1 and 50 chars"),
                age: int = Query(...,
                                 title="Person's age",
                                 description="This is the person's age. this is a required argument")):
    #  Query parameters (optionals) and required ...
    #  query parameters are optionals but can be used as needed
    return {name: age}


@app.get("/person/detail/{person_id}")
def show_person(person_id: int = Path(...,
                                      gt=0,
                                      title="Person's ID",
                                      description="Showing person's ID")):
    # validating path parameters
    return {person_id: "It exists"}


@app.put("/person/{person_id}")
def update_person(person_id: int = Path(...,
                                        gt=0,
                                        title="Person's ID",
                                        description="This is the person's ID"),
                  person: Person = Body(...),
                  location: Location = Body(...)):
    # validating path parameters
    # combine request bodies
    results = person.dict()
    results.update(location.dict())
    return {person_id: results}


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info")
