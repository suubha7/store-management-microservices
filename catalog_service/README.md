# Catalog Service

Catalog Service is part of the Store Management Microservices project.

It manages cities, product categories, products, and product availability for each city.

## Current Features

* Catalog Service project setup
* PostgreSQL database integration using Docker
* Docker Compose setup for Catalog API and Catalog PostgreSQL database
* City, category, product, and city-product database tables
* Pydantic request and response schemas
* Admin APIs for cities, categories, products, and city-product assignments
* Admin APIs to enable or disable cities, categories, products, and city-product availability
* Public catalog APIs to view active cities, categories, and available products by city
* Product filtering by city and category
* JWT protection for admin APIs
* Role-based admin authorization
* FastAPI service running on port `8002`
---

## 4. Add this section before `## Database Tables`

```md
## Docker Services

Catalog Service runs with two Docker containers:

```text
catalog-api
→ FastAPI Catalog Service
→ Exposed on http://127.0.0.1:8002

catalog-db
→ PostgreSQL database
→ Internal database for Catalog Service
```

## Database Tables

* `cities` — stores city details
* `categories` — stores product categories
* `products` — stores product information
* `cityproducts` — connects products with cities and controls availability

A product is created once in the `products` table. The `cityproducts` table decides whether that product is available in a specific city.

## Tech Stack

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* Docker
* Docker Compose
* Uvicorn
* uv


## Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://postgres:postgres@order-db:5432/order_db

SECRET_KEY=your_secret_key
ALGORITHM=HS256
```
## Run with Docker Compose

From the root `store-management-microservices` folder:

```bash
docker compose up --build catalog-db catalog-api
```

Open Swagger API documentation:

```text
http://127.0.0.1:8002/docs
```

## Next Features

* API Gateway integration
