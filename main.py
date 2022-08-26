"""
Run server: uvicorn main:app --reload
Open documentation in: http://127.0.0.1:5000/redoc or http://127.0.0.1:5000/docs"""
import uvicorn
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from fastapi import FastAPI, Body, Query, Path, Form, status, Header, Cookie

app = FastAPI()


# Create enums
class HairColor(Enum):
    WHITE = "white"
    BROWN = "brown"
    BLACK = "black"
    BLONDE = "blonde"
    RED = "red"


# Models
class Person(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    age: int = Field(..., gt=18, le=115)
    password: str = Field(..., min_length=8)
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)

    class Config:
        """Just for testing API. Default values shown in swagger, for example"""
        schema_extra = {
            "example": {
                "first_name": "Kenny",
                "last_name": "Miranda",
                "age": 27,
                "password": "12345678",
                "hair_color": HairColor.BLACK,
                "is_married": False,
                "email": "kenny@some.com"
            }
        }


class Location(BaseModel):
    city: str = Field(..., min_length=1, max_length=50, example="Queretaro")
    state: str = Field(..., min_length=1, max_length=50, example="Queretaro")
    country: str = Field(..., min_length=1, max_length=50, example="Mexico")


class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, example="AnomanderRK")
    message: str = Field(default="Login successfully!")


@app.get("/", status_code=status.HTTP_200_OK)
def home():
    return {"hello": "world"}


@app.post("/person/new", response_model=Person, response_model_exclude={"password"},
          status_code=status.HTTP_201_CREATED)
def create_person(person: Person = Body(...)):
    # request body. Body makes the parameter needed
    return person


@app.get("/person/detail", status_code=status.HTTP_200_OK)
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


@app.get("/person/detail/{person_id}", status_code=status.HTTP_200_OK)
def show_person(person_id: int = Path(...,
                                      gt=0,
                                      title="Person's ID",
                                      description="Showing person's ID")):
    # validating path parameters
    return {person_id: "It exists"}


@app.put("/person/{person_id}", status_code=status.HTTP_200_OK)
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


@app.post(path="/login", response_model=LoginOut, status_code=status.HTTP_200_OK)
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOut(username=username)


@app.post(path="/contact", status_code=status.HTTP_200_OK)
def contact(first_name: str = Form(..., max_length=20, min_length=1, example="Anomander"),
            last_name: str = Form(..., max_length=20, min_length=1, example="Rake"),
            email: EmailStr = Form(..., example="example@example.com"),
            message: str = Form(min_length=20, max_length=300, example="This is a message example ..."),
            user_agent: Optional[str] = Header(default=None),
            ads: Optional[str] = Cookie(default=None)):
    return {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "message": message,
        "user_agent": user_agent,
        "ads": ads,
    }


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info")
