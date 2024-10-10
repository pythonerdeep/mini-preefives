from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import engine, get_db
from .models import User, RewardHistory, Base
from pydantic import BaseModel

Base.metadata.create_all(bind=engine)

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

# Get All users
@app.get("/users")
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


# Create user
@app.post('/users/')
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(id=user.id, name=user.name, p5_balance=100, rewards_balance=0)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Edit user
@app.put("/users/{user_id}")
async def update_user(user_id: str, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.name = user.name
    db.commit()
    return db_user


# Create a P5 transaction
@app.post("/transactions/")
async def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    giver = db.query(User).filter(User.id == transaction.given_by_id).first()
    receiver = db.query(User).filter(User.id == transaction.given_to_id).first()

    if not giver or not receiver:
        raise HTTPException(status_code=404, detail="User not found")

    if giver.p5_balance < transaction.points:
        raise HTTPException(status_code=400, detail="Insufficient P5 balance")

    # Update balances
    giver.p5_balance -= transaction.points
    receiver.rewards_balance += transaction.points

    # Create transaction record
    reward_history = RewardHistory(
        given_by_id=transaction.given_by_id,
        given_to_id=transaction.given_to_id,
        points=transaction.points
    )
    db.add(reward_history)
    db.commit()
    return reward_history


# Get all transactions
@app.get("/transactions/")
async def get_transactions(db: Session = Depends(get_db)):
    transactions = db.query(RewardHistory).all()
    return transactions