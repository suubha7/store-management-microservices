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

Handles user accounts, authentication, and role-based access control.

* User registration
* Password hashing with bcrypt
* JWT authentication
* Protected user profile APIs
* Password change API
* User and admin roles
* Admin-only user management APIs

Status: Completed.

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
* User registration and email validation
* Password hashing and password verification
* JWT login and access-token generation
* Protected user profile APIs
* User profile update
* Password change API
* Role-based access control
* Admin-only APIs
* User activation/deactivation
* User deletion
* Pydantic validation
* Swagger API documentation

Next:

* Catalog Service
* Warehouse Service
* Order Service
* API Gateway
* PostgreSQL database container
* Docker containers and Docker Compose setup
