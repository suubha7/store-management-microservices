import os
import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, Request, Response, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.schema.user_schema import UserRegisterRequest,  UserUpdateRequest,ChangePasswordRequest
from app.dependencies import require_bearer_token

load_dotenv()

USERS_SERVICE_URL = os.getenv("USERS_SERVICE_URL")

user_gateway_router = APIRouter(prefix="/user", tags=["Users Gateway"])


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
            detail="Users Service is unavailable"
        )

    return Response(
        content=response.content,
        status_code=response.status_code,
        media_type=response.headers.get("content-type")
    )



@user_gateway_router.post("/register")
async def register_user(user_data: UserRegisterRequest, request: Request):
    return await forward_request(
        request,
        f"{USERS_SERVICE_URL}/user/register"
    )


@user_gateway_router.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{USERS_SERVICE_URL}/user/login",
                data={
                    "username": form_data.username,
                    "password": form_data.password
                },
                headers={
                    "content-type": "application/x-www-form-urlencoded"
                }
            )

    except httpx.ConnectError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Users Service is unavailable")

    return Response(
        content=response.content,
        status_code=response.status_code,
        media_type=response.headers.get("content-type")
    )



@user_gateway_router.get("/me", dependencies=[Depends(require_bearer_token)])
async def get_my_profile(request: Request):
    return await forward_request(
        request,
        f"{USERS_SERVICE_URL}/user/me"
    )


@user_gateway_router.put("/me", dependencies=[Depends(require_bearer_token)])
async def update_my_profile(user_data: UserUpdateRequest, request: Request):
    return await forward_request(
        request,
        f"{USERS_SERVICE_URL}/user/me"
    )


@user_gateway_router.put("/me/password", dependencies=[Depends(require_bearer_token)])
async def change_my_password(password_data: ChangePasswordRequest,request: Request):
    return await forward_request(
        request,
        f"{USERS_SERVICE_URL}/user/me/password"
    )