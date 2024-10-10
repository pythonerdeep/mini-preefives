# database.py
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from databases import Database

# SQLite database URL (SQLite file is stored locally)
DATABASE_URL = "sqlite:///./test.db"

# SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# For managing async queries
database = Database(DATABASE_URL)

# Base class for SQLAlchemy models
Base = declarative_base()
metadata = MetaData()
