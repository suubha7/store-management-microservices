from fastapi import FastAPI
from app.database import Base, engine
from app.models import Inventory
from app.routers.inventory_routers import inventory_router
from app.routers.inventory_internal_routers import inventory_internal_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventory Service")

# Root check endpoint
@app.get("/")
def read_root():

    return {
        "message": "Inventory Service is running"
    }

app.include_router(inventory_router)
app.include_router(inventory_internal_router)