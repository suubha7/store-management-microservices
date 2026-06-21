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
* Get user by ID
* Update user profile
* Get all users for admin
* Get user by ID for admin
* Activate or deactivate a user account
* Delete a user account
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
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── model.py
│   ├── schemas.py
│   ├── auth.py
│   ├── dependencies.py
│   └── routers/
│       ├── __init__.py
│       ├── user_router.py
│       └── admin_router.py
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

### Local Files Not Pushed to GitHub

```text
.venv/
users.db
__pycache__/
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
git clone https://github.com/suubha7/store-management-microservices.git
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
2. Test `POST /users/register` with a new email.
3. Test `POST /users/login` using the same registered email and password.
4. Test `GET /users/{user_id}` using the user ID returned after registration.
5. Test `PUT /users/{user_id}` and update one or more fields.

   Example request:

   ```json
   {
     "name": "Updated User Name",
     "city_id": 2
   }
   ```

6. Test `GET /users/{user_id}` again and confirm the updated data is returned.
7. Test password update using `PUT /users/{user_id}`.

   ```json
   {
     "password": "NewPassword123"
   }
   ```

8. Test `POST /users/login` with the old password and confirm that the API rejects it.
9. Test `POST /users/login` with the new password and confirm that login succeeds.
10. Try registering the same email again and confirm that the API rejects it.
11. Try login with an incorrect password and confirm that the API rejects it.
