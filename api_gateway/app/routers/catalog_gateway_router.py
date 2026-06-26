import os
import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, Request, Response, HTTPException, status

load_dotenv()

CATALOG_SERVICE_URL = os.getenv("CATALOG_SERVICE_URL")

catalog_gateway_router = APIRouter(
    prefix="/catalog",
    tags=["Catalog Gateway"]
)


# Forward HTTP request to service
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
            detail="Catalog Service is unavailable"
        )

    return Response(
        content=response.content,
        status_code=response.status_code,
        media_type=response.headers.get("content-type")
    )


# Retrieve all cities
@catalog_gateway_router.get("/cities")
async def get_cities(request: Request):
    return await forward_request(
        request,
        f"{CATALOG_SERVICE_URL}/catalog/cities"
    )


# Retrieve categories available in city
@catalog_gateway_router.get("/cities/{city_id}/categories")
async def get_categories_by_city(
    city_id: int,
    request: Request
):
    return await forward_request(
        request,
        f"{CATALOG_SERVICE_URL}/catalog/cities/{city_id}/categories"
    )


# Retrieve products available in city
@catalog_gateway_router.get("/cities/{city_id}/products")
async def get_products_by_city(
    city_id: int,
    request: Request
):
    return await forward_request(
        request,
        f"{CATALOG_SERVICE_URL}/catalog/cities/{city_id}/products"
    )


# Retrieve products in category
@catalog_gateway_router.get(
    "/cities/{city_id}/products/category/{category_id}"
)
async def get_products_by_category(
    city_id: int,
    category_id: int,
    request: Request
):
    return await forward_request(
        request,
        f"{CATALOG_SERVICE_URL}/catalog/cities/{city_id}/products/category/{category_id}"
    )


# Retrieve product details by ID
@catalog_gateway_router.get("/products/{product_id}")
async def get_product_by_id(
    product_id: int,
    request: Request
):
    return await forward_request(
        request,
        f"{CATALOG_SERVICE_URL}/catalog/products/{product_id}"
    )