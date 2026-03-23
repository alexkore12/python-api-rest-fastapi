# API Endpoints Reference

## Authentication

### POST /auth/login
```json
{
  "username": "user",
  "password": "password"
}
```
Returns: access_token

### POST /auth/refresh
Refresh expired token.

## Users

### GET /users
List all users (admin only)

### GET /users/{id}
Get user by ID

### POST /users
Create new user (admin only)

### PUT /users/{id}
Update user

### DELETE /users/{id}
Delete user (admin only)

## Items

### GET /items
List items (with pagination)

### POST /items
Create item (authenticated)

### GET /items/{id}
Get item by ID

## Health

### GET /health
Health check

### GET /metrics
Prometheus metrics

## Rate Limiting

- 100 requests/minute per IP
- 1000 requests/hour per user

