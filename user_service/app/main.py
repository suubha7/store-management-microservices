from fastapi import FastAPI
from app.routes.user_routes import user_router
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "message": "Users Service is running"
    }

app.include_router(user_router)