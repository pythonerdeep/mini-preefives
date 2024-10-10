from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import engine, database, get_db
from .models import User, RewardHistory
from pydantic import BaseModel

app = FastAPI()

# Pydantic Schemas
class UserCreate(BaseModel):
    id: str
    name: str

class UserUpdate(BaseModel):
    name: str

class TransactionCreate(BaseModel):
    given_by_id: str
    given_to_id: str
    points: int

# Dependency to get the database session
def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()


############## Route to create API #########################