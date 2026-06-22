# Users Service

Users Service is the first microservice in the Store Management Microservices project.

It manages user account registration and login for two roles:

* `user` — normal customer
* `admin` — store administrator

## Completed Features

* User registration
* Email validation
* Password hashing using bcrypt
* JWT authentication
* Login using OAuth2 form fields
* JWT token generation with user ID and role
* Protected user profile API
* Update own profile API
* Change own password API
* Admin-only APIs protected by JWT
* Get all users for admin
* Get user by ID for admin
* Activate or deactivate a user account
* Delete a user account
* Role-based access control (`user` and `admin`)
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
POST /user/login
```

Login uses OAuth2 form fields, not JSON.

```text
username = ravi@gmail.com
password = Ravi@123
```

During login:

1. The service finds the user by email from the `username` field.
2. The entered password is verified against the stored password hash.
3. The service checks whether the account is active.
4. The service creates and returns a JWT access token containing the user ID and role.

## Current Login Response

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "role": "user"
}
```


## Current Login Response

```json
{
  "message": "Login successful",
  "user_id": 1,
  "role": "user"
}
```

## JWT Authentication and Authorization

Protected endpoints require this header:

```text
Authorization: Bearer <access_token>
```

### User APIs

| Method | Endpoint            | Access         |
| ------ | ------------------- | -------------- |
| POST   | `/user/register`    | Public         |
| POST   | `/user/login`       | Public         |
| GET    | `/user/me`          | Logged-in user |
| PUT    | `/user/me`          | Logged-in user |
| PUT    | `/user/me/password` | Logged-in user |

### Admin APIs

| Method | Endpoint                        | Access     |
| ------ | ------------------------------- | ---------- |
| GET    | `/admin/users`                  | Admin only |
| GET    | `/admin/users/{user_id}`        | Admin only |
| PUT    | `/admin/users/status/{user_id}` | Admin only |
| DELETE | `/admin/users/{user_id}`        | Admin only |

### Access Rules

```text
No JWT token       → 401 Unauthorized
User JWT token     → can access only /user/me routes
User JWT token     → 403 Forbidden on /admin/* routes
Admin JWT token    → can access /admin/* routes
```


## Next Features

* API Gateway integration

## Run Tests Manually

1. Open Swagger UI at `http://127.0.0.1:8001/docs`.
2. Register a user using `POST /user/register` (provide email, password, name, city, etc.).
3. Login using `POST /user/login` with OAuth2 form fields:
   - `username`: registered email
   - `password`: registered password
4. Copy the returned `access_token` from the login response.
5. Click **Authorize** in Swagger and enter:
   ```text
   Bearer <access_token>
   ```
6. Test `GET /user/me`.  
   **Expected:** `200 OK` with the current user's profile data.
7. Test `PUT /user/me` by updating fields such as `name` or `city`.  
   **Expected:** `200 OK` and the updated profile returned.
8. Test `PUT /user/me/password` by providing old and new passwords.  
   **Expected:** success response (e.g., `200 OK`).
9. Log out (or clear the Authorization header) and attempt to login using the old password.  
   **Expected:** `401 Unauthorized`.
10. Login again using the new password.  
    **Expected:** successful JWT response (new `access_token`).
11. Remove the Authorization header (or do not send a token) and call `GET /user/me`.  
    **Expected:** `401 Unauthorized`.
12. With a **normal user** token (the one from step 4), call `GET /admin/users`.  
    **Expected:** `403 Forbidden`.
13. Login using an **admin** account (you may need to create one manually or via a seed script).  
    Copy the admin `access_token` and authorize Swagger with it (replace the previous token).
14. Call `GET /admin/users` with the admin token.  
    **Expected:** `200 OK` with a list of all users.
15. Test `PUT /admin/users/status/{user_id}` by choosing a user ID (e.g., the normal user from step 2) and sending:  
    ```json
    {
      "is_active": false
    }
