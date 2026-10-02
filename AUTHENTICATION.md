# Authentication and Security

## Authentication

JWT-based authentication is used.

Password security uses bcrypt.

## Customer Flow

```text
Register
   ↓
Validate fields
   ↓
Hash password
   ↓
Save user
   ↓
Login
   ↓
Verify password
   ↓
Generate JWT
```

## Protected Routes

Authenticated customer routes require a valid JWT.

Admin routes require:
1. Valid JWT
2. Admin authorization

## Middleware

### Auth Middleware

Purpose:
- Read JWT
- Verify JWT
- Identify authenticated user
- Protect private routes

### Admin Middleware

Purpose:
- Check authenticated user's admin role
- Allow access to admin routes only

## Validation

Required validations:
- Required fields
- Valid email
- Password minimum 6 characters
- Unique email
- Positive product price
- Non-negative stock
- Valid category

## Important Security Rule

Never trust the product price sent by the frontend.

The backend must fetch the current product price from MongoDB before creating an order.

## Logout

Logout should remove the client's stored authentication state/token according to the application's authentication handling.
