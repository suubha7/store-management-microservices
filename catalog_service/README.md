# Catalog Service

## Overview

Catalog Service manages cities, product categories, products, and product availability for each city in the Store Management Microservices project.

It provides public catalog APIs for customers and protected admin APIs for managing catalog data.

---

## Responsibilities

- Manage cities
- Manage product categories
- Manage products
- Assign products to cities
- Control product availability by city
- Provide active catalog data to customers
- Provide product name and price to Order Service during checkout
- Enforce admin access for catalog management

---

## Architecture / Communication

```text
Frontend / API Gateway
        │
        ▼
  Catalog Service
        │
        ▼
   Catalog Database
        │
        └── Order Service requests product name and price during checkout
```

The API Gateway forwards public and admin catalog requests to this service.

Order Service calls Catalog Service internally to get the real product name, price, and availability during checkout.

---

## Features

- Create cities
- Enable or disable cities
- Create categories
- Update categories
- Enable or disable categories
- Create products
- Update products
- Enable or disable products
- Assign products to cities
- Enable or disable city-product availability
- Public APIs for active cities, categories, and available products
- Filter products by city and category
- Admin-only catalog management APIs
- JWT authentication and role-based authorization
- PostgreSQL database through Docker

---

## API Endpoints

### Public APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /catalog/cities | Get active cities |
| GET | /catalog/cities/{city_id}/categories | Get active categories for a city |
| GET | /catalog/cities/{city_id}/products | Get available products for a city |
| GET | /catalog/cities/{city_id}/products/category/{category_id} | Get products by city and category |
| GET | /catalog/products/{product_id} | Get product details |

### Admin City APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /admin/cities | Get all cities |
| GET | /admin/cities/{city_id} | Get city by ID |
| POST | /admin/city | Create city |
| PUT | /admin/city/{city_id}/status | Enable or disable city |

### Admin Category APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /admin/categories | Get all categories |
| GET | /admin/categories/{category_id} | Get category by ID |
| POST | /admin/categories | Create category |
| PUT | /admin/categories/{category_id} | Update category |
| PUT | /admin/categories/{category_id}/status | Enable or disable category |

### Admin Product APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /admin/products | Get all products |
| GET | /admin/products/{product_id} | Get product by ID |
| POST | /admin/products | Create product |
| PUT | /admin/products/{product_id} | Update product |
| PUT | /admin/products/{product_id}/status | Enable or disable product |

### Admin City-Product APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /admin/city-products | Get all city-product mappings |
| GET | /admin/city-products/{city_product_id} | Get mapping by ID |
| POST | /admin/city-products | Assign product to city |
| PUT | /admin/city-products/{city_product_id}/availability | Change availability |
| DELETE | /admin/city-products/{city_product_id} | Remove mapping |

---

## Authentication and Authorization

Public routes:

```
GET /catalog/*
```

Admin routes require:

```
Authorization: Bearer <admin_access_token>
```

Access rules:

```
No token    → 401 Unauthorized for admin routes
User token  → 403 Forbidden for admin routes
Admin token → can access /admin/* routes
```

---

## Environment Variables

Create a `.env` file inside `catalog_service/`.

```env
DATABASE_URL=postgresql://USER_NAME:PASSWORD@catalog-db:5432/catalog_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
```

> `SECRET_KEY` and `ALGORITHM` must match Users, Inventory, and Order services so the same JWT token can be validated across services.

---

## Run with Docker Compose

From the project root:

```bash
docker compose up --build catalog-db catalog-api
```

To run the complete project:

```bash
docker compose up --build
```

---

## Swagger URL

Direct service Swagger:

```
http://127.0.0.1:8002/docs
```

Recommended Gateway Swagger:

```
http://127.0.0.1:8000/docs
```

---

## Project Structure

```
catalog_service/
├── app/
│   ├── routers/
│   │   ├── admin_router.py
│   │   └── catalog_router.py
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   ├── models.py
│   └── schemas/
│       ├── city_schema.py
│       ├── category_schema.py
│       ├── product_schema.py
│       └── city_product_schema.py
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
2. Add the admin JWT token in Swagger or Postman
3. Create a city
4. Create a category
5. Create a product
6. Assign the product to the city
7. Call public catalog APIs without a token
8. Confirm the city, category, and product appear
9. Disable a city, category, product, or mapping
10. Confirm unavailable data is not returned by public APIs

---

## Current Status

Completed.

This service is integrated with API Gateway and is used by Order Service during checkout to fetch real product details and price.