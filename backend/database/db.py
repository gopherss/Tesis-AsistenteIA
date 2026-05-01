from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Final
from os import getenv
from dotenv import load_dotenv

load_dotenv()

DEV_URL: Final[str] = "postgresql://user:pass@localhost:5432/example_db"
DATABASE_URL: Final[str] = getenv("DATABASE_URL", DEV_URL)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
