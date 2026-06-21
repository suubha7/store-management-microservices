# Users Service

Users Service is the first microservice in the Store Management Microservices project.

It manages user account registration and login for two roles:

* `user` — normal customer
* `admin` — store administrator

## Completed Features

* User registration
* Email validation
* Password hashing using bcrypt
* User login
* Password verification
* SQLite database integration
* Pydantic request validation
* Swagger API documentation

## Tech Stack

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* Passlib with bcrypt
* Uvicorn

## Project Structure

```text
users-service/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   └── routers/
│       └── user_router.py
├── requirements.txt
└── users.db
```

## User Database Fields

| Field           | Description           |
| --------------- | --------------------- |
| `id`            | Unique user ID        |
| `name`          | User name             |
| `email`         | Unique login email    |
| `password_hash` | Hashed password       |
| `city_id`       | Selected city ID      |
| `role`          | `user` or `admin`     |
| `is_active`     | Account status        |
| `created_at`    | Account creation time |

## Installation

Clone the repository and move into the project folder.

```bash
git clone <your-repository-url>
cd users-service
```

Install project dependencies:

```bash
uv sync
```

## Run the Service

```bash
uv run uvicorn app.main:app --reload --port 8001
```

The service runs at:

```text
http://127.0.0.1:8001
```

Swagger documentation:

```text
http://127.0.0.1:8001/docs
```

## APIs

### Register User

```text
POST /users/register
```

Request body:

```json
{
  "name": "Ravi Kumar",
  "email": "ravi@gmail.com",
  "password": "Ravi@123",
  "city_id": 1
}
```

During registration:

1. The service checks whether the email already exists.
2. The password is hashed using bcrypt.
3. The user is saved in the SQLite database.
4. The role is automatically set to `user`.

### Login User

```text
POST /users/login
```

Request body:

```json
{
  "email": "ravi@gmail.com",
  "password": "Ravi@123"
}
```

During login:

1. The service finds the user by email.
2. The entered password is verified against the stored password hash.
3. The service returns a successful login response with the user ID and role.

## Current Login Response

```json
{
  "message": "Login successful",
  "user_id": 1,
  "role": "user"
}
```

## Next Features

* JWT authentication
* Protected user profile APIs
* Admin-only APIs
* PostgreSQL database container
* Docker container for the FastAPI service
* Integration with API Gateway

## Run Tests Manually

1. Open Swagger UI at `http://127.0.0.1:8001/docs`.
2. Test `POST /users/register`.
3. Test `POST /users/login` using the same email and password.
4. Try registering the same email again and confirm that the API rejects it.
5. Try login with an incorrect password and confirm that the API rejects it.
