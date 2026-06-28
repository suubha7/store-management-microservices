import pytest
from app.database import Base, get_db
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from fastapi.testclient import TestClient
from app.main import app
from app.auth import hash_password
from app.model import User

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit= False, autoflush= False, bind= engine)

def get_override_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# override the actual db with the test db
app.dependency_overrides[get_db] = get_override_db

@pytest.fixture(scope="function")
def client():
    Base.metadata.create_all(bind= engine)
    yield TestClient(app)

    Base.metadata.drop_all(bind= engine)


@pytest.fixture(scope="function")
def user_headers(client):
    data = {
        "name": "Subham",
        "email": "subham@gmail.com",
        "password": "test123",
        "city_id": 1
    }
    client.post("/user/register", json=data)
    
    payload = {
        "username": "subham@gmail.com",
        "password": "test123"
    }

    login = client.post("/user/login", data=payload)
    token = login.json()['access_token']

    return {
        "Authorization": f"Bearer {token}"
    }

@pytest.fixture
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def admin_headers(client, db):

    admin = User(
        name="Admin",
        email="admin@gmail.com",
        hashed_password=hash_password("admin123"),
        role="admin",
        city_id=1,
        is_active=True
    )

    db.add(admin)
    db.commit()

    # Login through the API
    response = client.post(
        "/user/login",
        data={
            "username": "admin@gmail.com",
            "password": "admin123"
        }
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }
