import os
import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, Request, Response, HTTPException, status, Depends
from app.dependencies import require_bearer_token
from app.schema.catalog_schema import (
    CityCreateRequest, 
    CityStatusUpdateRequest,
    CategoryCreateRequest, CategoryUpdateRequest, CategoryStatusUpdateRequest,
    CityProductCreateRequest, CityProductAvailabilityUpdateRequest,
    ProductCreateRequest, ProductUpdateRequest, ProductStatusUpdateRequest
)
from app.schema.inventory_schema import CreateInventoryRequest, InventoryStockUpdateRequest

load_dotenv()

USERS_SERVICE_URL = os.getenv("USERS_SERVICE_URL")
CATALOG_SERVICE_URL = os.getenv("CATALOG_SERVICE_URL")
INVENTORY_SERVICE_URL = os.getenv("INVENTORY_SERVICE_URL")
ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL")

admin_gateway_router = APIRouter(
    prefix="/admin",
    tags=["Admin Gateway"],
    dependencies=[Depends(require_bearer_token)]
)


async def forward_request(request: Request, url: str):
    headers = {}

    if request.headers.get("content-type"):
        headers["content-type"] = request.headers.get("content-type")

    if request.headers.get("authorization"):
        headers["authorization"] = request.headers.get("authorization")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=request.method,
                url=url,
                params=request.query_params,
                content=await request.body(),
                headers=headers
            )

    except httpx.ConnectError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Target service is unavailable"
        )

    return Response(
        content=response.content,
        status_code=response.status_code,
        media_type=response.headers.get("content-type")
    )


@admin_gateway_router.get("/users")
async def get_all_users(request: Request):
    return await forward_request(
        request,
        f"{USERS_SERVICE_URL}/admin/users"
    )


@admin_gateway_router.get("/users/{user_id}")
async def get_user_by_id(user_id: int, request: Request):
    return await forward_request(
        request,
        f"{USERS_SERVICE_URL}/admin/user/{user_id}"
    )


@admin_gateway_router.put("/users/{user_id}/status")
async def update_user_status(user_id: int, request: Request):
    return await forward_request(
        request,
        f"{USERS_SERVICE_URL}/admin/user/update_status/{user_id}"
    )


@admin_gateway_router.delete("/users/{user_id}")
async def delete_user(user_id: int, request: Request):
    return await forward_request(
        request,
        f"{USERS_SERVICE_URL}/admin/user/delete/{user_id}"
    )


@admin_gateway_router.get("/catalog/cities")
async def get_cities(request: Request):
    return await forward_request(
        request,
        f"{CATALOG_SERVICE_URL}/admin/cities"
    )


@admin_gateway_router.get("/catalog/cities/{city_id}")
async def get_city_by_id(city_id: int, request: Request):
    return await forward_request(
        request,
        f"{CATALOG_SERVICE_URL}/admin/cities/{city_id}"
    )


@admin_gateway_router.post("/catalog/city")
async def create_city(city_date: CityCreateRequest,request: Request):
    return await forward_request(
        request,
        f"{CATALOG_SERVICE_URL}/admin/city"
    )


@admin_gateway_router.put("/catalog/city/{city_id}/status")
async def update_city_status(city_id: int, city_data: CityStatusUpdateRequest, request: Request):
    return await forward_request(
        request,
        f"{CATALOG_SERVICE_URL}/admin/city/{city_id}/status"
    )


@admin_gateway_router.get("/catalog/categories")
async def get_categories(request: Request):
    return await forward_request(
        request,
        f"{CATALOG_SERVICE_URL}/admin/categories"
    )


@admin_gateway_router.get("/catalog/categories/{category_id}")
async def get_category_by_id(category_id: int, request: Request):
    return await forward_request(
        request,
        f"{CATALOG_SERVICE_URL}/admin/categories/{category_id}"
    )


@admin_gateway_router.post("/catalog/categories")
async def create_category(catalog_data: CategoryCreateRequest, request: Request):
    return await forward_request(
        request,
        f"{CATALOG_SERVICE_URL}/admin/categories"
    )


@admin_gateway_router.put("/catalog/categories/{category_id}")
async def update_category(category_id: int, catalog_data: CategoryUpdateRequest, request: Request):
    return await forward_request(
        request,
        f"{CATALOG_SERVICE_URL}/admin/categories/{category_id}"
    )


@admin_gateway_router.put("/catalog/categories/{category_id}/status")
async def update_category_status(category_id: int, catalog_data: CategoryStatusUpdateRequest, request: Request):
    return await forward_request(
        request,
        f"{CATALOG_SERVICE_URL}/admin/categories/{category_id}/status"
    )


@admin_gateway_router.get("/catalog/products")
async def get_products(request: Request):
    return await forward_request(
        request,
        f"{CATALOG_SERVICE_URL}/admin/products"
    )


@admin_gateway_router.get("/catalog/products/{product_id}")
async def get_product_by_id(product_id: int, request: Request):
    return await forward_request(
        request,
        f"{CATALOG_SERVICE_URL}/admin/products/{product_id}"
    )


@admin_gateway_router.post("/catalog/products")
async def create_product(product_data: ProductCreateRequest, request: Request):
    return await forward_request(
        request,
        f"{CATALOG_SERVICE_URL}/admin/products"
    )


@admin_gateway_router.put("/catalog/products/{product_id}")
async def update_product(product_id: int, product_data: ProductUpdateRequest, request: Request):
    return await forward_request(
        request,
        f"{CATALOG_SERVICE_URL}/admin/products/{product_id}"
    )


@admin_gateway_router.put("/catalog/products/{product_id}/status")
async def update_product_status(product_id: int, product_data: ProductStatusUpdateRequest, request: Request):
    return await forward_request(
        request,
        f"{CATALOG_SERVICE_URL}/admin/products/{product_id}/status"
    )



@admin_gateway_router.get("/catalog/city-products")
async def get_city_products(request: Request):
    return await forward_request(
        request,
        f"{CATALOG_SERVICE_URL}/admin/city-products"
    )


@admin_gateway_router.get("/catalog/city-products/{city_product_id}")
async def get_city_product_by_id(
    city_product_id: int,
    request: Request
):
    return await forward_request(
        request,
        f"{CATALOG_SERVICE_URL}/admin/city-products/{city_product_id}"
    )


@admin_gateway_router.post("/catalog/city-products")
async def create_city_product(cityproduct_data: CityProductCreateRequest, request: Request):
    return await forward_request(
        request,
        f"{CATALOG_SERVICE_URL}/admin/city-products"
    )


@admin_gateway_router.put("/catalog/city-products/{city_product_id}/availability")
async def update_city_product_availability(
    city_product_id: int,
    cityproduct_data: CityProductAvailabilityUpdateRequest,
    request: Request
):
    return await forward_request(
        request,
        f"{CATALOG_SERVICE_URL}/admin/city-products/{city_product_id}/availability"
    )


@admin_gateway_router.delete("/catalog/city-products/{city_product_id}")
async def delete_city_product(
    city_product_id: int,
    request: Request
):
    return await forward_request(
        request,
        f"{CATALOG_SERVICE_URL}/admin/city-products/{city_product_id}"
    )



@admin_gateway_router.get("/inventory/inventories")
async def get_inventories(request: Request):
    return await forward_request(
        request,
        f"{INVENTORY_SERVICE_URL}/admin/inventories"
    )


@admin_gateway_router.post("/inventory/inventories")
async def create_inventory(inventory_data:CreateInventoryRequest, request: Request):
    return await forward_request(
        request,
        f"{INVENTORY_SERVICE_URL}/admin/inventories"
    )


@admin_gateway_router.get("/inventory/inventories/{inventory_id}")
async def get_inventory_by_id(
    inventory_id: int,
    request: Request
):
    return await forward_request(
        request,
        f"{INVENTORY_SERVICE_URL}/admin/inventories/{inventory_id}"
    )


@admin_gateway_router.put("/inventory/inventories/{inventory_id}")
async def update_inventory(
    inventory_id: int,
    inventory_data: InventoryStockUpdateRequest,
    request: Request
):
    return await forward_request(
        request,
        f"{INVENTORY_SERVICE_URL}/admin/inventories/{inventory_id}"
    )


@admin_gateway_router.delete("/inventory/inventories/{inventory_id}")
async def delete_inventory(
    inventory_id: int,
    request: Request
):
    return await forward_request(
        request,
        f"{INVENTORY_SERVICE_URL}/admin/inventories/{inventory_id}"
    )



@admin_gateway_router.get("/orders")
async def get_all_orders(request: Request):
    return await forward_request(
        request,
        f"{ORDER_SERVICE_URL}/admin/orders"
    )


@admin_gateway_router.get("/orders/{order_id}")
async def get_order_by_id(
    order_id: int,
    request: Request
):
    return await forward_request(
        request,
        f"{ORDER_SERVICE_URL}/admin/orders/{order_id}"
    )