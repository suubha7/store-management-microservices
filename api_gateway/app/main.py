from fastapi import FastAPI

from app.routers.user_gateway_router import user_gateway_router
from app.routers.catalog_gateway_router import catalog_gateway_router
from app.routers.inventory_gateway_router import inventory_gateway_router
from app.routers.order_gateway_router import order_gateway_router
from app.routers.admin_gateway_router import admin_gateway_router


app = FastAPI(
    title="Store Management API Gateway",
    version="0.1.0"
)


@app.get("/")
def read_root():
    return {
        "message": "API Gateway is running"
    }


app.include_router(user_gateway_router)
app.include_router(catalog_gateway_router)
app.include_router(inventory_gateway_router)
app.include_router(order_gateway_router)
app.include_router(admin_gateway_router)