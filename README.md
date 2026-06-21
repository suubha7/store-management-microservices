# Store Management Microservices

Store management system built with FastAPI and microservices.

The project has two panels:

* User Panel
* Admin Panel

## Project Structure

```text
store-management-microservices/
├── api-gateway/
├── users-service/
├── catalog-service/
├── warehouse-service/
├── order-service/
├── docker-compose.yml
└── README.md
```

## Services

### Users Service

Handles user registration and login.

* Password hashing
* User and admin roles
* JWT authentication will be added later

Status: Completed basic registration and login.

### Catalog Service

Manages city-based catalogs and products.

* Cities
* Catalogs
* Products
* Product prices

Status: Planned.

### Warehouse Service

Manages product stock for each city.

* Add stock
* Reduce stock
* Check available stock
* Low-stock products

Status: Planned.

### Order Service

Manages customer orders.

* Create order
* Check product price
* Check stock
* Reduce stock after order
* View order status

Status: Planned.

### API Gateway

The single entry point for all client requests.

```text
/users/*      → Users Service
/cities/*     → Catalog Service
/catalogs/*   → Catalog Service
/products/*   → Catalog Service
/inventory/*  → Warehouse Service
/orders/*     → Order Service
```

Status: Planned.

## User and Admin Access

### User Panel

A user can:

* Register and login
* Select city
* View products
* Check stock
* Create an order
* View own orders

### Admin Panel

An admin can:

* Manage cities
* Manage catalogs and products
* Manage stock
* View all orders
* Manage users

## Architecture

```text
User Panel / Admin Panel
          ↓
      API Gateway
          ↓
Users Service
Catalog Service
Warehouse Service
Order Service
```

Each service will have its own database.

## Technology

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* SQLite for local development
* PostgreSQL for Docker deployment
* Docker
* Docker Compose
* Uvicorn
* uv

## Current Progress

Completed:

* Users Service setup
* SQLite database connection
* User registration
* Password hashing
* User login
* User profile
* User update
* Pydantic validation
* Swagger API documentation
* Admin APIs

Next:

* JWT authentication
* Catalog Service
* Warehouse Service
* Order Service
* API Gateway
* Docker Compose setup
