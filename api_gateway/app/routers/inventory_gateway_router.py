import os
import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, Request, Response, HTTPException, status

load_dotenv()

INVENTORY_SERVICE_URL = os.getenv("INVENTORY_SERVICE_URL")

inventory_gateway_router = APIRouter(
    prefix="/inventory",
    tags=["Inventory Gateway"]
)


# Forward HTTP request to service
async def forward_request(
    request: Request,
    url: str
):
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
            detail="Inventory Service is unavailable"
        )

    return Response(
        content=response.content,
        status_code=response.status_code,
        media_type=response.headers.get("content-type")
    )


# Forward check stock request
@inventory_gateway_router.post("/check-stock")
async def forward_check_stock(
    request: Request
):
    return await forward_request(
        request,
        f"{INVENTORY_SERVICE_URL}/inventory/check-stock"
    )


# Forward reduce stock request
@inventory_gateway_router.post("/reduce-stock")
async def forward_reduce_stock(
    request: Request
):
    return await forward_request(
        request,
        f"{INVENTORY_SERVICE_URL}/inventory/reduce-stock"
    )