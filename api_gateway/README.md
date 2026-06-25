# Store Management API Gateway

The API Gateway is the single entry point for the Store Management Microservices project.

It receives requests from the frontend or API client and forwards them to the correct microservice.

## Architecture

```text
Frontend / Postman / Swagger
            |
            v
      API Gateway :8000
            |
   --------------------------------
   |              |               |
Users Service  Catalog Service  Order Service
                                   |
                                   v
                            Inventory Service
```

The frontend communicates only with the API Gateway.

## Current Gateway Responsibilities

* Routes requests to the correct microservice
* Forwards request body, query parameters, and HTTP method
* Forwards the `Authorization` header
* Returns the target service response to the client
* Provides one central Swagger API documentation page

## Current Scope

This version is a lightweight proxy gateway.

It does not yet contain:

* Gateway Pydantic request schemas
* Gateway-level JWT validation
* Swagger `Authorize` button support
* CORS configuration for frontend
* Rate limiting
* Centralized logging
* Retry handling

Each microservice remains responsible for:

* JWT validation
* Role validation
* Request validation
* Business rules
* Database operations

## Services

| Service           | Internal Docker URL         | Responsibility                                           |
| ----------------- | --------------------------- | -------------------------------------------------------- |
| Users Service     | `http://users-api:8000`     | Registration, login, user profile, admin user management |
| Catalog Service   | `http://catalog-api:8000`   | Cities, categories, products, city-product mapping       |
| Inventory Service | `http://inventory-api:8000` | Inventory CRUD, stock check, stock reduction             |
| Order Service     | `http://order-api:8000`     | Cart, checkout, customer orders, admin orders            |

## Public Gateway Routes

### Users

```text
POST /user/register
POST /user/login
GET  /user/me
PUT  /user/me
PUT  /user/me/password
```

### Catalog

```text
GET /catalog/cities
GET /catalog/cities/{city_id}/categories
GET /catalog/cities/{city_id}/products
GET /catalog/cities/{city_id}/products/category/{category_id}
GET /catalog/products/{product_id}
```

### Cart

```text
POST   /cart/items
GET    /cart
PUT    /cart/items/{cart_item_id}
DELETE /cart/items/{cart_item_id}
DELETE /cart/clear
```

### Orders

```text
POST /orders/checkout
GET  /orders
GET  /orders/{order_id}
```

### Admin

```text
GET    /admin/users
GET    /admin/users/{user_id}
PUT    /admin/users/{user_id}/status
DELETE /admin/users/{user_id}

GET  /admin/catalog/cities
GET  /admin/catalog/cities/{city_id}
POST /admin/catalog/city
PUT  /admin/catalog/city/{city_id}/status

GET  /admin/catalog/categories
GET  /admin/catalog/categories/{category_id}
POST /admin/catalog/categories
PUT  /admin/catalog/categories/{category_id}
PUT  /admin/catalog/categories/{category_id}/status

GET  /admin/catalog/products
GET  /admin/catalog/products/{product_id}
POST /admin/catalog/products
PUT  /admin/catalog/products/{product_id}
PUT  /admin/catalog/products/{product_id}/status

GET    /admin/catalog/city-products
GET    /admin/catalog/city-products/{city_product_id}
POST   /admin/catalog/city-products
PUT    /admin/catalog/city-products/{city_product_id}/availability
DELETE /admin/catalog/city-products/{city_product_id}

GET    /admin/inventory/inventories
POST   /admin/inventory/inventories
GET    /admin/inventory/inventories/{inventory_id}
PUT    /admin/inventory/inventories/{inventory_id}
DELETE /admin/inventory/inventories/{inventory_id}

GET /admin/orders
GET /admin/orders/{order_id}
```

## Internal Routes Not Exposed Through Gateway

These routes are called only by Order Service through the Docker network.

```text
POST /inventory/check-stock
POST /inventory/reduce-stock
```

The customer must not access these routes directly.

## Environment Variables

Create a `.env` file inside `api_gateway/`.

```env
USERS_SERVICE_URL=http://users-api:8000
CATALOG_SERVICE_URL=http://catalog-api:8000
INVENTORY_SERVICE_URL=http://inventory-api:8000
ORDER_SERVICE_URL=http://order-api:8000
```

The names `users-api`, `catalog-api`, `inventory-api`, and `order-api` must match the Docker Compose service names.

## Run With Docker Compose

From the project root:

```bash
docker compose up --build
```

Open Gateway Swagger:

```text
http://127.0.0.1:8000/docs
```

## Authentication

Public routes:

```text
POST /user/register
POST /user/login
GET  /catalog/...
```

Protected routes require this header:

```http
Authorization: Bearer <access_token>
```

The Gateway forwards this header to the target service.

JWT validation is currently performed inside each microservice, not in the Gateway.


## Next Improvements

* Add Gateway request schemas for POST, PUT, and PATCH routes
* Add Swagger bearer authorization support
* Add CORS for frontend integration
* Add frontend application

