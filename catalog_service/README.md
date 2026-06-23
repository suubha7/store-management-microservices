# Catalog Service

Catalog Service is part of the Store Management Microservices project.

It manages cities, product categories, products, and product availability for each city.

## Current Features

* Catalog Service project setup
* SQLite database connection
* City, category, product, and city-product database tables
* Pydantic request and response schemas
* Admin APIs for cities, categories, products, and city-product assignments
* Admin APIs to enable or disable cities, categories, products, and city-product availability
* Public catalog APIs to view active cities, categories, and available products by city
* Product filtering by city and category
* FastAPI service running on port `8002`

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
* SQLite
* Uvicorn
* uv

## Run Locally

```bash
uv sync
uv run uvicorn app.main:app --reload --port 8002
```

Open Swagger API documentation:

```text
http://127.0.0.1:8002/docs
```

## Next Features

* JWT protection for admin APIs
* Role-based admin authorization
* PostgreSQL database migration
* Docker container support
* API Gateway integration
