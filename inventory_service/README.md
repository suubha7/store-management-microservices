# Inventory Service

## Overview

Inventory Service manages product stock for each city in the Store Management Microservices project.

It provides protected admin APIs for inventory management and internal APIs used by Order Service during checkout.

---

## Responsibilities

- Create inventory records for city-product pairs
- View inventory records
- Update stock quantity
- Delete inventory records
- Check stock before checkout
- Reduce stock after successful checkout
- Prevent duplicate inventory records for the same city and product
- Enforce admin access for inventory management
- Protect internal inventory APIs from public access

---

## Architecture / Communication

```text
Admin / API Gateway
        │
        ▼
 Inventory Service
        │
        ▼
 Inventory Database

Order Service
        │
        ├── POST /inventory/check-stock
        └── POST /inventory/reduce-stock
```

The API Gateway forwards admin inventory requests to this service.

Order Service calls the internal stock APIs through Docker networking during checkout.

---

## Features

- Create inventory for a city and product
- Get all inventory records
- Get inventory by ID
- Update stock quantity
- Delete inventory record
- Duplicate city-product inventory validation
- Check available stock
- Reduce stock after checkout
- Admin-only inventory CRUD APIs
- Internal service authentication for stock APIs
- PostgreSQL database through Docker

---

## Inventory Data

| Field | Description |
|-------|-------------|
| id | Inventory record ID |
| city_id | City ID from Catalog Service |
| product_id | Product ID from Catalog Service |
| stock_quantity | Available quantity |
| created_at | Record creation time |
| updated_at | Last update time |

Each `city_id` and `product_id` pair can have only one inventory record.

Inventory Service stores Catalog Service IDs as normal integer values. It does not use cross-service foreign keys.

---

## API Endpoints

### Admin Inventory APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /admin/inventories | Get all inventory records |
| POST | /admin/inventories | Create inventory record |
| GET | /admin/inventories/{inventory_id} | Get inventory by ID |
| PUT | /admin/inventories/{inventory_id} | Update stock quantity |
| DELETE | /admin/inventories/{inventory_id} | Delete inventory record |

### Internal Order Service APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /inventory/check-stock | Check product stock for a city |
| POST | /inventory/reduce-stock | Reduce stock after checkout |

> Internal routes are called by Order Service only. They are not exposed through the API Gateway.

---

## Authentication and Authorization

Admin routes require:

```
Authorization: Bearer <admin_access_token>
```

Internal Order Service routes require:

```
X-Internal-Service-Key: <internal_service_key>
```

Access rules:

```
No JWT token         → 401 Unauthorized for admin routes
User JWT token       → 403 Forbidden for admin routes
Admin JWT token      → can access /admin/* routes
Missing internal key → 401 Unauthorized for internal routes
Invalid internal key → 403 Forbidden for internal routes
```

---

## Environment Variables

Create a `.env` file inside `inventory_service/`.

```env
DATABASE_URL=postgresql://USER_NAME:PASSWORD@inventory-db:5432/inventory_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
INTERNAL_SERVICE_KEY=your_internal_service_key
```

> `SECRET_KEY` and `ALGORITHM` must match Users, Catalog, and Order services.
> `INTERNAL_SERVICE_KEY` must match the value in Order Service.

---

## Run with Docker Compose

From the project root:

```bash
docker compose up --build inventory-db inventory-api
```

To run the complete project:

```bash
docker compose up --build
```

---

## Swagger URL

Direct service Swagger:

```
http://127.0.0.1:8003/docs
```

Recommended Gateway Swagger for admin APIs:

```
http://127.0.0.1:8000/docs
```

---

## Project Structure

```
inventory_service/
├── app/
│   ├── routers/
│   │   ├── inventory_router.py
│   │   └── internal_inventory_router.py
│   ├── schema/
│   │   └── inventory_schema.py
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   └── models.py
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
- Docker
- Docker Compose
- Uvicorn

---

## Testing Flow

1. Login with an admin account
2. Add admin JWT token
3. Create inventory using `city_id`, `product_id`, and `stock_quantity`
4. Get all inventory records
5. Update stock quantity
6. Call Order Service checkout
7. Confirm stock quantity is reduced
8. Try checkout with quantity greater than stock
9. Confirm checkout fails with insufficient stock
10. Confirm internal stock routes reject requests without internal service key

---

## Current Status

Completed.

This service is integrated with API Gateway for admin APIs and with Order Service for stock checking and stock reduction during checkout.