# Catalog Service

Catalog Service is part of the Store Management Microservices project.

It manages cities, product categories, products, and product availability for each city.

## Current Features

* Catalog Service project setup
* SQLite database connection
* City table
* Category table
* Product table
* City product availability table
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

* Pydantic schemas
* Admin APIs for cities, categories, and products
* Public APIs to view city products
* JWT protection for admin APIs
* PostgreSQL and Docker support
