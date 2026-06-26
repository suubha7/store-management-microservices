from fastapi import FastAPI

from app.database import Base, engine
from app import models

from app.routers.cart_routers import cart_router
from app.routers.order_routers import order_router
from app.routers.admin_order_routers import admin_order_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Order Service")


# Root check endpoint
@app.get("/")
def read_root():
    return {
        "message": "Order Service is running"
    }


app.include_router(cart_router)
app.include_router(order_router)
app.include_router(admin_order_router)

