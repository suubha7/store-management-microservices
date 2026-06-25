import os
import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, Request, Response, HTTPException, status, Depends
from app.dependencies import require_bearer_token
from app.schema.order_schema import CartItemCreateRequest, CartItemUpdateRequest, CheckoutRequest

load_dotenv()

ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL")

order_gateway_router = APIRouter(
    tags=["Order Gateway"],
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
            detail="Order Service is unavailable"
        )

    return Response(
        content=response.content,
        status_code=response.status_code,
        media_type=response.headers.get("content-type")
    )



@order_gateway_router.post("/cart/items")
async def create_cart_item(item_data:CartItemCreateRequest, request: Request):
    return await forward_request(
        request,
        f"{ORDER_SERVICE_URL}/cart/items"
    )


@order_gateway_router.get("/cart")
async def get_cart_items(request: Request):
    return await forward_request(
        request,
        f"{ORDER_SERVICE_URL}/cart"
    )


@order_gateway_router.put("/cart/items/{cart_item_id}")
async def update_cart_item(
    cart_item_id: int,
    item_data: CartItemUpdateRequest,
    request: Request
):
    return await forward_request(
        request,
        f"{ORDER_SERVICE_URL}/cart/items/{cart_item_id}"
    )


@order_gateway_router.delete("/cart/items/{cart_item_id}")
async def delete_cart_item(
    cart_item_id: int,
    request: Request
):
    return await forward_request(
        request,
        f"{ORDER_SERVICE_URL}/cart/items/{cart_item_id}"
    )


@order_gateway_router.delete("/cart/clear")
async def clear_cart(request: Request):
    return await forward_request(
        request,
        f"{ORDER_SERVICE_URL}/cart/clear"
    )


@order_gateway_router.post("/orders/checkout")
async def checkout(checkout_data: CheckoutRequest, request: Request):
    return await forward_request(
        request,
        f"{ORDER_SERVICE_URL}/orders/checkout"
    )


@order_gateway_router.get("/orders")
async def get_my_orders(request: Request):
    return await forward_request(
        request,
        f"{ORDER_SERVICE_URL}/orders"
    )


@order_gateway_router.get("/orders/{order_id}")
async def get_my_order_by_id(
    order_id: int,
    request: Request
):
    return await forward_request(
        request,
        f"{ORDER_SERVICE_URL}/orders/{order_id}"
    )