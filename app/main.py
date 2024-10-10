from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import engine, get_db
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



############## Route to create API #########################

# Create user
@app.post('/users/')
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(id=user.id, name=user.name, p5_balance=100, rewards_balance=0)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user