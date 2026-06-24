# Order Service

Order Service manages the user cart and order checkout process for the Store Management Microservices project.

## Features

* Add products to cart
* View cart items
* Update cart quantity
* Remove cart items
* Clear cart
* Checkout from cart
* Create orders and order items
* View user orders
* Admin can view all orders
* JWT authentication for users and admins
* Gets product name and price from Catalog Service
* Checks and reduces stock using Inventory Service

## Services Used

* Users Service for JWT authentication
* Catalog Service for product details and price
* Inventory Service for stock checking and stock reduction

## API Endpoints

### Cart APIs

* `POST /cart/items`
* `GET /cart`
* `PUT /cart/items/{cart_item_id}`
* `DELETE /cart/items/{cart_item_id}`
* `DELETE /cart/clear`

### User Order APIs

* `POST /orders/checkout`
* `GET /orders`
* `GET /orders/{order_id}`

### Admin Order APIs

* `GET /admin/orders`
* `GET /admin/orders/{order_id}`

## Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your_secret_key
ALGORITHM=HS256
CATALOG_SERVICE_URL=http://127.0.0.1:8002
INVENTORY_SERVICE_URL=http://127.0.0.1:8003
```

## Run the Service

Install dependencies:

```bash
uv sync
```

Run the server:

```bash
uv run uvicorn app.main:app --reload --port 8004
```

Open Swagger API documentation:

```text
http://127.0.0.1:8004/docs
```

## Checkout Flow

```text
User adds products to cart
→ User sends checkout request with city ID
→ Order Service gets product name and price from Catalog Service
→ Order Service checks stock from Inventory Service
→ Inventory Service reduces stock
→ Order Service creates order and order items
→ Cart is cleared
```

## Tech Stack

* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* JWT
* HTTPX
* UV
