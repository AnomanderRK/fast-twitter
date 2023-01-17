from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    birthday = Column(Date)
    tweets = relationship("Tweet", back_populates="by")


class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String)
    by = relationship("User", back_populates="tweets")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))
