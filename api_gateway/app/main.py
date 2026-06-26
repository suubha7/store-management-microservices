from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.user_gateway_router import user_gateway_router
from app.routers.catalog_gateway_router import catalog_gateway_router
from app.routers.inventory_gateway_router import inventory_gateway_router
from app.routers.order_gateway_router import order_gateway_router
from app.routers.admin_gateway_router import admin_gateway_router


app = FastAPI(
    title="Store Management API Gateway",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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