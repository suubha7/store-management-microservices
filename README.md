# Store Management Microservices

A backend store-management system built with **FastAPI** using a microservices architecture.

The system supports two roles:

- **Customer** — register, login, browse products, manage cart, checkout, and view orders.
- **Admin** — manage cities, categories, products, city-product availability, inventory, users, and orders.

All client requests go through the **API Gateway**. Individual microservices communicate internally through Docker networking.

---

## Architecture

```
    Frontend / Swagger 
            │
            ▼
       API Gateway
            │
 ┌──────────┼───────────┬──────────────┐
 ▼          ▼           ▼              ▼
Users    Catalog     Inventory       Order
Service  Service      Service       Service
  │         │            │              │
Users DB  Catalog DB  Inventory DB    Order DB
```

### Service Communication — Customer Checkout Flow

```
Customer checkout
    │
    ▼
API Gateway
    │
    ▼
Order Service
    ├── Catalog Service: fetch product name, price, and availability
    ├── Inventory Service: check stock
    ├── Inventory Service: reduce stock
    ├── Order Database: create order and order items
    └── Cart: clear cart after successful checkout
```

> Each microservice owns its database. Services store external IDs such as `user_id`, `city_id`, and `product_id` as normal integer values. Cross-service database foreign keys are not used.

---

## Project Structure

```
store-management-microservices/
├── api_gateway/
│   ├── app/
│   │   ├── routers/
│   │   ├── schemas/
│   │   ├── dependencies.py
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── users_service/
│   ├── app/
│   ├── Dockerfile
│   └── requirements.txt
│
├── catalog_service/
│   ├── app/
│   ├── Dockerfile
│   └── requirements.txt
│
├── inventory_service/
│   ├── app/
│   ├── Dockerfile
│   └── requirements.txt
│
├── order_service/
│   ├── app/
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yml
└── README.md
```

---

## Services

### 1. Users Service

Responsible for authentication, user accounts, and role-based access control.

**Features:**
- User registration with city selection
- Password hashing using bcrypt
- JWT login and access token generation
- Protected profile APIs
- Update profile
- Change password
- User and admin roles
- Admin user management
- Activate / deactivate users
- Delete users

---

### 2. Catalog Service

Responsible for cities, categories, products, and city-product availability.

**Features:**
- Create and manage cities
- Create and manage categories
- Create and manage products
- Assign products to cities
- Enable or disable city, category, product, and city-product availability
- Public APIs for active cities, categories, and products
- Filter products by city and category
- Admin-only catalog APIs

---

### 3. Inventory Service

Responsible for product stock for each city.

**Features:**
- Create inventory for a city-product pair
- View inventory records
- Update stock quantity
- Delete inventory records
- Prevent duplicate city-product inventory records
- Internal stock check endpoint for Order Service
- Internal stock reduction endpoint after checkout
- Admin-only inventory APIs
- Internal service key protection for service-to-service routes

---

### 4. Order Service

Responsible for carts, checkout, and orders.

**Features:**
- Add items to cart
- Update cart quantity
- Remove cart item
- Clear cart
- View current cart
- Checkout cart
- Create orders and order items
- View customer orders
- Admin can view all orders
- Fetches product name and price from Catalog Service using HTTPX
- Checks and reduces stock through Inventory Service using HTTPX
- Clears cart after successful checkout

---

### 5. API Gateway

The single public entry point for frontend, Swagger, and Postman.

**Features:**
- Explicit Gateway routes
- Request schemas for POST, PUT, and PATCH APIs
- Swagger request-body documentation
- JWT Bearer token support in Swagger
- Forwards JWT headers to microservices
- Gateway validates request format
- Microservices perform final JWT, role, and business-rule validation

**Public Gateway URL:**
```
http://127.0.0.1:8000
```

**Swagger documentation:**
```
http://127.0.0.1:8000/docs
```

---

## Main Gateway Routes

### User Routes

```
POST   /user/register
POST   /user/login
GET    /user/me
PUT    /user/me
PUT    /user/me/password
```

### Public Catalog Routes

```
GET    /catalog/cities
GET    /catalog/categories
GET    /catalog/products
GET    /catalog/products/{product_id}
```

### Customer Cart and Order Routes

```
GET    /cart
POST   /cart/items
PUT    /cart/items/{cart_item_id}
DELETE /cart/items/{cart_item_id}
DELETE /cart/clear

POST   /orders/checkout
GET    /orders
GET    /orders/{order_id}
```

### Admin Catalog Routes

```
POST   /admin/catalog/city
PUT    /admin/catalog/city/{city_id}/status

POST   /admin/catalog/categories
PUT    /admin/catalog/categories/{category_id}
PUT    /admin/catalog/categories/{category_id}/status

POST   /admin/catalog/products
PUT    /admin/catalog/products/{product_id}
PUT    /admin/catalog/products/{product_id}/status

POST   /admin/catalog/city-products
PUT    /admin/catalog/city-products/{city_product_id}/availability
```

### Admin Inventory Routes

```
GET    /admin/inventory/inventories
POST   /admin/inventory/inventories
GET    /admin/inventory/inventories/{inventory_id}
PUT    /admin/inventory/inventories/{inventory_id}
DELETE /admin/inventory/inventories/{inventory_id}
```

### Admin Order and User Routes

```
GET    /admin/orders
GET    /admin/users
PUT    /admin/users/{user_id}/status
DELETE /admin/users/{user_id}
```

---

## Authentication Flow

1. User logs in through `POST /user/login`
2. Users Service returns an access token
3. Frontend sends the token with protected requests:

```
Authorization: Bearer <access_token>
```

4. API Gateway forwards the `Authorization` header
5. Target microservice validates JWT and role permissions

### Access Levels

| Route Pattern | Requirement |
|---|---|
| `POST /user/register`, `POST /user/login`, `GET /catalog/*` | No token required (public) |
| `/user/me`, `/cart/*`, `/orders/*` | Valid user token |
| `/admin/*` | Valid admin token |

---

## Admin Setup Flow

Before customers can place orders, an admin must create data in this order:

1. Create city
2. Create category
3. Create product
4. Assign product to city
5. Create inventory record for city and product
6. Add stock quantity

**Example:**

```
City:                Hyderabad
Category:            Electronics
Product:             Wireless Mouse
City-Product Mapping: Hyderabad + Wireless Mouse
Inventory:           Hyderabad + Wireless Mouse + Stock 100
```

---

## Customer Order Flow

1. Register and login
2. Browse products for selected city
3. Add product to cart
4. Checkout using `city_id`
5. Order Service fetches current product price from Catalog Service
6. Order Service checks stock from Inventory Service
7. Order Service reduces stock
8. Order and order items are created
9. Cart is cleared
10. Customer can view the order

---

## Technology Stack

| Layer | Technology |
|---|---|
| Language | Python |
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Validation | Pydantic |
| Auth | JWT + bcrypt |
| Inter-service HTTP | HTTPX |
| Database | PostgreSQL |
| Containerization | Docker + Docker Compose |
| Server | Uvicorn |
| API Docs | Swagger / OpenAPI |

---

## Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/suubha7/store-management-microservices
cd store-management-microservices
```

### 2. Create environment files

Create `.env` files for each service using the required database URLs, JWT settings, service URLs, and internal service key.

**Example — Order Service `.env`:**

```env
CATALOG_SERVICE_URL=http://catalog-api:8000
INVENTORY_SERVICE_URL=http://inventory-api:8000
INTERNAL_SERVICE_KEY=your_internal_secret_key
```

> The same `INTERNAL_SERVICE_KEY` must be configured in both Order Service and Inventory Service.

### 3. Start all containers

```bash
docker compose up --build
```

### 4. Open Gateway Swagger

```
http://127.0.0.1:8000/docs
```

---

## Testing Flow

Use Gateway Swagger.

1. Register an admin user
2. Login as admin
3. Create city, category, product, city-product mapping, and inventory
4. Login as a customer
5. Add a product to cart
6. Checkout
7. Confirm order was created
8. Confirm cart was cleared
9. Confirm inventory stock was reduced
10. Login as admin and confirm all orders are visible

---

## Current Status

### Completed

- Users Service
- Catalog Service
- Inventory Service
- Order Service
- API Gateway
- JWT authentication
- Role-based authorization
- Cart and checkout flow
- Catalog-to-Order HTTPX communication
- Inventory stock check and reduction
- Docker Compose setup
- PostgreSQL databases
- Gateway Swagger request schemas
- End-to-end backend testing

### Next Phase

- Frontend application
- Product images