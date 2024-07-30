from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost/TodoApplicationDatabase"

engine  = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit = False,autoflush=False,bind=engine)

Base = declarative_base()
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
