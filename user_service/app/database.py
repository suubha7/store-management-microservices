from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./users.db")


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionUser = sessionmaker(autocommit= False, autoflush= False, bind= engine)

Base = declarative_base()

def get_db():
    db = SessionUser()
    try:
        yield db
    finally:
        db.close()