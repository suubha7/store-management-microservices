# API Gateway

## Overview

API Gateway is the single public entry point for the Store Management Microservices project.

Frontend, Swagger, and Postman send requests only to API Gateway. The Gateway forwards each request to the correct microservice.

---

## Responsibilities

- Receive all client API requests
- Route requests to the correct microservice
- Forward request body, query parameters, HTTP method, and headers
- Forward the `Authorization` JWT header
- Provide one central Swagger API documentation page
- Validate request body format using Pydantic schemas
- Require a Bearer token header for protected Gateway routes
- Return the target service response to the client

---

## Architecture / Communication

```text
Frontend / Swagger / Postman
            │
            ▼
       API Gateway :8000
            │
 ┌──────────┼───────────┬──────────────┐
 ▼          ▼           ▼              ▼
Users    Catalog     Inventory       Order
Service  Service      Service       Service
```

The frontend must call only API Gateway.

```
Correct:
Frontend → API Gateway → Microservice

Incorrect:
Frontend → Users Service directly
Frontend → Catalog Service directly
Frontend → Inventory Service directly
Frontend → Order Service directly
```

---

## Features

- Explicit routes for Users, Catalog, Cart, Orders, and Admin APIs
- Gateway request schemas for POST and PUT routes
- Swagger request body documentation
- Swagger Bearer token authorization support
- Authorization header forwarding
- Request body forwarding
- Query parameter forwarding
- HTTP method forwarding
- Service unavailable handling
- One public Gateway URL for frontend integration

---

## Service Routes

| Gateway Area | Target Service |
|---|---|
| /user/* | Users Service |
| /catalog/* | Catalog Service |
| /cart/* | Order Service |
| /orders/* | Order Service |
| /admin/users/* | Users Service |
| /admin/catalog/* | Catalog Service |
| /admin/inventory/* | Inventory Service |
| /admin/orders/* | Order Service |

---

## API Endpoints

### User APIs

| Method | Gateway Endpoint | Target Service Endpoint |
|--------|------------------|------------------------|
| POST | /user/register | Users Service /user/register |
| POST | /user/login | Users Service /user/login |
| GET | /user/me | Users Service /user/me |
| PUT | /user/me | Users Service /user/me |
| PUT | /user/me/password | Users Service /user/me/password |

### Public Catalog APIs

| Method | Gateway Endpoint | Description |
|--------|------------------|-------------|
| GET | /catalog/cities | Get active cities |
| GET | /catalog/cities/{city_id}/categories | Get categories for city |
| GET | /catalog/cities/{city_id}/products | Get products for city |
| GET | /catalog/cities/{city_id}/products/category/{category_id} | Get products by city and category |
| GET | /catalog/products/{product_id} | Get product details |

### Cart APIs

| Method | Gateway Endpoint | Description |
|--------|------------------|-------------|
| GET | /cart | Get current user cart |
| POST | /cart/items | Add product to cart |
| PUT | /cart/items/{cart_item_id} | Update cart item |
| DELETE | /cart/items/{cart_item_id} | Remove cart item |
| DELETE | /cart/clear | Clear cart |

### Order APIs

| Method | Gateway Endpoint | Description |
|--------|------------------|-------------|
| POST | /orders/checkout | Checkout cart |
| GET | /orders | Get current user orders |
| GET | /orders/{order_id} | Get order by ID |

### Admin User APIs

| Method | Gateway Endpoint | Description |
|--------|------------------|-------------|
| GET | /admin/users | Get all users |
| GET | /admin/users/{user_id} | Get user by ID |
| PUT | /admin/users/{user_id}/status | Update user status |
| DELETE | /admin/users/{user_id} | Delete user |

### Admin Catalog APIs

| Method | Gateway Endpoint | Description |
|--------|------------------|-------------|
| GET | /admin/catalog/cities | Get all cities |
| GET | /admin/catalog/cities/{city_id} | Get city by ID |
| POST | /admin/catalog/city | Create city |
| PUT | /admin/catalog/city/{city_id}/status | Update city status |
| GET | /admin/catalog/categories | Get all categories |
| GET | /admin/catalog/categories/{category_id} | Get category by ID |
| POST | /admin/catalog/categories | Create category |
| PUT | /admin/catalog/categories/{category_id} | Update category |
| PUT | /admin/catalog/categories/{category_id}/status | Update category status |
| GET | /admin/catalog/products | Get all products |
| GET | /admin/catalog/products/{product_id} | Get product by ID |
| POST | /admin/catalog/products | Create product |
| PUT | /admin/catalog/products/{product_id} | Update product |
| PUT | /admin/catalog/products/{product_id}/status | Update product status |
| GET | /admin/catalog/city-products | Get city-product mappings |
| GET | /admin/catalog/city-products/{city_product_id} | Get mapping by ID |
| POST | /admin/catalog/city-products | Assign product to city |
| PUT | /admin/catalog/city-products/{city_product_id}/availability | Update availability |
| DELETE | /admin/catalog/city-products/{city_product_id} | Delete mapping |

### Admin Inventory APIs

| Method | Gateway Endpoint | Description |
|--------|------------------|-------------|
| GET | /admin/inventory/inventories | Get inventory records |
| POST | /admin/inventory/inventories | Create inventory |
| GET | /admin/inventory/inventories/{inventory_id} | Get inventory by ID |
| PUT | /admin/inventory/inventories/{inventory_id} | Update inventory stock |
| DELETE | /admin/inventory/inventories/{inventory_id} | Delete inventory |

### Admin Order APIs

| Method | Gateway Endpoint | Description |
|--------|------------------|-------------|
| GET | /admin/orders | Get all orders |
| GET | /admin/orders/{order_id} | Get order by ID |

---

## Authentication and Authorization

Public routes:

```
POST /user/register
POST /user/login
GET  /catalog/*
```

Protected customer routes:

```
GET /user/me
PUT /user/me
PUT /user/me/password
/cart/*
/orders/*
```

Protected admin routes:

```
/admin/*
```

Protected routes require:

```
Authorization: Bearer <access_token>
```

---

## Swagger Authorization

1. Call `POST /user/login`
2. Copy the `access_token`
3. Click **Authorize** in Gateway Swagger
4. Paste only the token value
5. Click **Authorize**
6. Call protected routes

> The Gateway checks that a Bearer token exists and forwards it.
> The target microservice performs final JWT validation, role validation, and business-rule validation.

---

## Internal Routes

These Inventory Service routes are not exposed through API Gateway:

```
POST /inventory/check-stock
POST /inventory/reduce-stock
```

Order Service calls them internally through Docker networking during checkout.

Customers must not call these routes directly.

---

## Environment Variables

Create a `.env` file inside `api_gateway/`.

```env
USERS_SERVICE_URL=http://users-api:8000
CATALOG_SERVICE_URL=http://catalog-api:8000
INVENTORY_SERVICE_URL=http://inventory-api:8000
ORDER_SERVICE_URL=http://order-api:8000
```

> The Docker service names must match `docker-compose.yml`.

---

## Run with Docker Compose

From the project root:

```bash
docker compose up --build
```

To rebuild only Gateway:

```bash
docker compose up --build api-gateway
```

---

## Swagger URL

```
http://127.0.0.1:8000/docs
```

---

## Project Structure

```
api_gateway/
├── app/
│   ├── routers/
│   │   ├── user_gateway_router.py
│   │   ├── catalog_gateway_router.py
│   │   ├── order_gateway_router.py
│   │   └── admin_gateway_router.py
│   ├── schemas/
│   │   ├── user_schema.py
│   │   ├── catalog_schema.py
│   │   ├── inventory_schema.py
│   │   ├── cart_schema.py
│   │   └── order_schema.py
│   ├── dependencies.py
│   └── main.py
├── Dockerfile
├── requirements.txt
├── .env
└── README.md
```

---

## Tech Stack

- Python
- FastAPI
- HTTPX
- Pydantic
- JWT Bearer authentication
- Docker
- Docker Compose
- Uvicorn

---

## Testing Flow

1. Start all containers using Docker Compose
2. Open `http://127.0.0.1:8000/docs`
3. Register a customer and admin user
4. Login as admin
5. Add admin token using Swagger Authorize
6. Create city, category, product, city-product mapping, and inventory
7. Login as customer
8. Add customer token using Swagger Authorize
9. Browse catalog
10. Add product to cart
11. Checkout
12. Confirm order created, cart cleared, and stock reduced
13. Login as admin and confirm all orders are visible

---

## Current Status

Completed.

API Gateway is integrated with Users Service, Catalog Service, Inventory Service, and Order Service. The complete backend flow works through:

```
http://127.0.0.1:8000
```