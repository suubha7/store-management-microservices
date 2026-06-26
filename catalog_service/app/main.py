from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routers.admin.city_routers import city_router
from app.routers.admin.category_routers import category_router
from app.routers.admin.product_routers import product_router
from app.routers.admin.city_product_router import city_product_router
from app.routers.catalog_routers import catalog_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Catalog Service")

# Root check endpoint
@app.get("/")
def read_root():
    return {
        "message": "Catalog Service is running"
    }

app.include_router(city_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(city_product_router)
app.include_router(catalog_router)