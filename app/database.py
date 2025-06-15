from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()                                              # pulls in .env during local dev

# Use an env var so you never check creds into git
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://user:password@localhost:3306/boochi",
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,            # handles dropped DB connections gracefully
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is imported by models.py
Base = declarative_base()
