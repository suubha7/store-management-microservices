from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL =os.getenv("DATABASE_URL", "sqlite:///./catalogs.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit= False, autoflush= False, bind=engine)
Base = declarative_base()

# Get database session dependency
def get_db():
    db = SessionLocal()

    try: 
        yield db
    finally:
        db.close()
