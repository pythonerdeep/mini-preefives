from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import engine, database
from .models import Base, User

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()

# Connect to the database on startup
@app.on_event("startup")
async def startup():
    await database.connect()

# Disconnect from the database on shutdown
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Route to create API