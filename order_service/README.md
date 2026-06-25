# Order Service

## Overview

Order Service manages customer carts, checkout, and orders for the Store Management Microservices project.

During checkout, it calls Catalog Service to get the current product name and price, then calls Inventory Service to check and reduce stock.

---

## Responsibilities

- Manage customer carts
- Add, update, remove, and clear cart items
- Create orders from cart items
- Get real product details and price from Catalog Service
- Check stock through Inventory Service
- Reduce stock through Inventory Service
- Clear cart after successful checkout
- Allow customers to view their own orders
- Allow admins to view all orders

---

## Architecture / Communication

```text
Customer / API Gateway
        │
        ▼
   Order Service
        │
        ├── Order Database
        │
        ├── Catalog Service
        │     └── Gets product name and price
        │
        └── Inventory Service
              ├── Checks stock
              └── Reduces stock
```

The API Gateway forwards customer cart and order requests to this service.

Order Service uses HTTPX for internal communication with Catalog Service and Inventory Service.

---

## Features

- Add product to cart
- View current cart
- Update cart item quantity
- Remove cart item
- Clear cart
- Checkout from cart
- Create order and order items
- View current user orders
- View order by ID
- Admin can view all orders
- JWT authentication for customer and admin routes
- HTTPX calls to Catalog Service
- HTTPX calls to Inventory Service
- Internal service key used for Inventory Service calls
- PostgreSQL database through Docker

---

## Checkout Flow

1. Customer adds products to cart
2. Customer sends checkout request with `city_id`
3. Order Service gets product name and price from Catalog Service
4. Order Service checks stock from Inventory Service
5. Inventory Service reduces stock
6. Order Service creates order and order items
7. Order Service clears the cart
8. Customer can view the created order

---

## API Endpoints

### Customer Cart APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /cart | Get current user cart |
| POST | /cart/items | Add product to cart |
| PUT | /cart/items/{cart_item_id} | Update cart item quantity |
| DELETE | /cart/items/{cart_item_id} | Remove cart item |
| DELETE | /cart/clear | Clear current user cart |

### Customer Order APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /orders/checkout | Checkout cart and create order |
| GET | /orders | Get current user orders |
| GET | /orders/{order_id} | Get current user order by ID |

### Admin Order APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /admin/orders | Get all orders |
| GET | /admin/orders/{order_id} | Get order by ID |

---

## Authentication and Authorization

Customer routes require:

```
Authorization: Bearer <access_token>
```

Admin routes require:

```
Authorization: Bearer <admin_access_token>
```

Access rules:

```
No token    → 401 Unauthorized
User token  → can access /cart/* and /orders/* routes
User token  → 403 Forbidden for /admin/* routes
Admin token → can access /admin/orders routes
```

---

## Environment Variables

Create a `.env` file inside `order_service/`.

```env
DATABASE_URL=postgresql://USER_NAME:PASSWORD@order-db:5432/order_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
CATALOG_SERVICE_URL=http://catalog-api:8000
INVENTORY_SERVICE_URL=http://inventory-api:8000
INTERNAL_SERVICE_KEY=your_internal_service_key
```

> `SECRET_KEY` and `ALGORITHM` must match Users, Catalog, and Inventory services.
> `INTERNAL_SERVICE_KEY` must match the value in Inventory Service.

---

## Run with Docker Compose

From the project root:

```bash
docker compose up --build order-db order-api
```

To run the complete project:

```bash
docker compose up --build
```

---

## Swagger URL

Direct service Swagger:

```
http://127.0.0.1:8004/docs
```

Recommended Gateway Swagger:

```
http://127.0.0.1:8000/docs
```

---

## Project Structure

```
order_service/
├── app/
│   ├── routers/
│   │   ├── cart_router.py
│   │   ├── order_router.py
│   │   └── admin_order_router.py
│   ├── services/
│   │   ├── catalog_client.py
│   │   └── inventory_client.py
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   ├── models.py
│   └── schemas/
│       ├── cart_schema.py
│       └── order_schema.py
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
- HTTPX
- Docker
- Docker Compose
- Uvicorn

---

## Testing Flow

1. Login as admin
2. Create city, category, product, city-product mapping, and inventory
3. Login as customer
4. Add product to cart
5. View cart
6. Call `POST /orders/checkout` with `city_id`
7. Confirm order is created
8. Confirm cart is cleared
9. Confirm inventory stock is reduced
10. Call `GET /orders`
11. Login as admin and call `GET /admin/orders`

---

## Current Status

Completed.

This service is integrated with API Gateway, Catalog Service, and Inventory Service. It handles the complete customer checkout workflow.