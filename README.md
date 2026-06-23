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
├── inventory-service/
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

Manages cities, categories, products, and product availability by city.

* City management
* Product category management
* Product catalog management
* Product availability for each city
* Admin APIs for cities, categories, products, and city-product assignments
* Public APIs to view active cities, categories, and available products by city
* Product filtering by city and category
* JWT authentication and admin-role authorization for all `/admin/*` APIs
* Public `/catalog/*` APIs remain accessible without JWT

Status: Completed.

### Inventory Service

Manages product stock for each city.

* Create inventory records for a city and product
* View all inventory records
* View inventory by ID
* Update stock quantity
* Delete inventory records
* JWT authentication and admin-role authorization for all inventory admin APIs

Inventory stores `city_id` and `product_id` from Catalog Service as normal IDs. It has its own database and does not use cross-service foreign keys.

Status: Completed.

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
/inventory/*  → Inventory Service
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
* Manage inventory stock by city and product
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
Inventory Service
Order Service
```

Each service has its own database.

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
* Catalog Service project setup
* Catalog Service SQLite database connection
* Catalog Service database models: City, Category, Product, and CityProduct
* Catalog Service Pydantic request and response schemas
* Catalog Service admin APIs for cities, categories, products, and city-product assignments
* Catalog Service status management for cities, categories, products, and city-product availability
* Catalog Service public APIs for active cities, categories, products, and category-based product filtering
* JWT protection and role-based authorization for Catalog Service admin APIs
* Catalog Service running on port `8002`
* Inventory Service project setup
* Inventory Service SQLite database connection
* Inventory Service database model: Inventory
* Inventory Service Pydantic request and response schemas
* Inventory Service admin APIs for creating, viewing, updating, and deleting inventory records
* Inventory Service duplicate city-product inventory validation
* JWT protection and admin-role authorization for Inventory Service admin APIs
* Inventory Service running on port `8003`

## Next

* Order Service
* API Gateway
* PostgreSQL database container
* Docker containers and Docker Compose setup
