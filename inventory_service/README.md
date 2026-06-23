# Inventory Service

Inventory Service manages product stock for each city in the store-management microservices project.

## Features

* Create stock for a product in a city
* View all inventory records
* View inventory by ID
* Update stock quantity
* Delete inventory records
* JWT-based admin authorization

## Project Structure

```text
inventory-service/
│
├── app/
│   ├── routers/
│   │   └── inventory_router.py
│   │
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── dependencies.py
│   └── schema/
│       └── inventory_schema.py
│
├── .env
├── .gitignore
├── pyproject.toml
├── uv.lock
├── inventory.db
└── README.md
```


## Inventory Table

| Field          | Description                     |
| -------------- | ------------------------------- |
| id             | Inventory record ID             |
| city_id        | City ID from Catalog Service    |
| product_id     | Product ID from Catalog Service |
| stock_quantity | Available product quantity      |
| created_at     | Record creation time            |
| updated_at     | Last update time                |

Each city and product pair can have only one inventory record.

## API Endpoints

| Method | Endpoint                            | Description               |
| ------ | ----------------------------------- | ------------------------- |
| GET    | `/admin/inventories`                | Get all inventory records |
| POST   | `/admin/inventories`                | Create inventory record   |
| GET    | `/admin/inventories/{inventory_id}` | Get inventory by ID       |
| PUT    | `/admin/inventories/{inventory_id}` | Update stock quantity     |
| DELETE | `/admin/inventories/{inventory_id}` | Delete inventory record   |

## Authentication

All admin endpoints require a JWT token with:

```text
role = admin
```

The service uses the same `SECRET_KEY` and `ALGORITHM` as Users Service and Catalog Service.

## Run the Service

```bash
uv run uvicorn app.main:app --reload --port 8003
```

Open Swagger API docs:

```text
http://127.0.0.1:8003/docs
```
