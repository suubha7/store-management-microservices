# Users Service

## Overview

Users Service manages user accounts, authentication, and role-based access control for the Store Management Microservices project.
It is responsible for user registration, login, JWT access tokens, profile management, and admin user management.

---

## Responsibilities

- Register users
- Hash and verify passwords
- Login using OAuth2 form data
- Generate JWT access tokens
- Manage user profiles
- Change passwords
- Enforce user and admin roles
- Allow admins to manage user accounts

---

## Architecture / Communication

```text
Frontend / API Gateway
        │
        ▼
   Users Service
        │
        ▼
     Users Database
```

The API Gateway forwards client requests to this service.
Other services use the JWT created by Users Service to validate customer and admin access.

---

## Features

- User registration with name, email, password, and city_id
- Email validation
- Password hashing using bcrypt
- JWT authentication
- OAuth2 login form
- Access token includes user ID and role
- Get current user profile
- Update current user profile
- Change current user password
- Admin can view users
- Admin can activate or deactivate users
- Admin can delete users
- Role-based access control for user and admin
- PostgreSQL database through Docker

---

## API Endpoints

### Public APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /user/register | Register a new user |
| POST | /user/login | Login and receive JWT token |

### Customer APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /user/me | Get current user profile |
| PUT | /user/me | Update current user profile |
| PUT | /user/me/password | Change current user password |

### Admin APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /admin/users | Get all users |
| GET | /admin/users/{user_id} | Get user by ID |
| PUT | /admin/users/{user_id}/status | Activate or deactivate user |
| DELETE | /admin/users/{user_id} | Delete user |

---

## Authentication and Authorization

Public routes:

```
POST /user/register
POST /user/login
```

Protected routes require:

```
Authorization: Bearer <access_token>
```

Access rules:

```
User token  → can access /user/me routes
Admin token → can access /admin/users routes
User token  → receives 403 Forbidden for admin routes
No token    → receives 401 Unauthorized for protected routes
```

---

## Environment Variables

Create a `.env` file inside `users_service/`.

```env
DATABASE_URL=postgresql://USER_NAME:PASSWORD@users-db:5432/users_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

> `SECRET_KEY` and `ALGORITHM` must match the values used by Catalog, Inventory, and Order services so they can validate the same JWT token.

---

## Run with Docker Compose

From the project root:

```bash
docker compose up --build users-db users-api
```

To run the complete project:

```bash
docker compose up --build
```

---

## Swagger URL

Direct service Swagger:

```
http://127.0.0.1:8001/docs
```

Recommended Gateway Swagger:

```
http://127.0.0.1:8000/docs
```

---

## Project Structure

```
users_service/
├── app/
│   ├── routers/
│   │   ├── user_router.py
│   │   └── admin_router.py
│   ├── auth.py
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── Dockerfile
├── requirements.txt
├── .env
└── README.md
```

---

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL
- JWT
- bcrypt
- Docker
- Docker Compose
- Uvicorn

---

## Testing Flow

1. Register a user using `POST /user/register`
2. Login using `POST /user/login`
3. Copy `access_token` from the response
4. Send `Authorization: Bearer <access_token>`
5. Test `GET /user/me`
6. Test `PUT /user/me`
7. Test `PUT /user/me/password`
8. Login with an admin account
9. Test `GET /admin/users`
10. Test user status update and delete routes

---

## Current Status

Completed.
This service is integrated with API Gateway and used by the complete Store Management Microservices backend.