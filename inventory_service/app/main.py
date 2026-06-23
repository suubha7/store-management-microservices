from fastapi import FastAPI
from app.database import Base, engine
from app.models import Inventory
from app.routers.inventory_routers import inventory_router

Base.metadata.create_all(bind=engine)

app = FastAPI(tags=["Inventory APIs"])

@app.get("/")
def read_root():

    return {
        "message": "Inventory Service is running"
    }

app.include_router(inventory_router)