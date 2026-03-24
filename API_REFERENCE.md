# API Reference — Python REST API (FastAPI)

> **Base URL:** `http://localhost:8000`  
> **Authentication:** Bearer token (JWT) via `Authorization: Bearer <token>`  
> **Content-Type:** `application/json` for all POST/PUT requests

---

## Authentication

### POST /auth/login

Login y obtener access token.

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "secret"}'
```

**Response `200`:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

**Response `401` — Invalid credentials:**
```json
{
  "detail": "Incorrect username or password"
}
```

---

### POST /auth/refresh

Refrescar un token expirado.

```bash
curl -X POST http://localhost:8000/auth/refresh \
  -H "Authorization: Bearer <refresh_token>"
```

**Response `200`:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

---

## Users

### GET /users

Listar todos los usuarios (requiere rol `admin`).

```bash
curl -X GET http://localhost:8000/users \
  -H "Authorization: Bearer <token>"
```

**Response `200`:**
```json
[
  {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "is_active": true,
    "role": "admin"
  }
]
```

---

### GET /users/{id}

Obtener usuario por ID.

```bash
curl -X GET http://localhost:8000/users/1 \
  -H "Authorization: Bearer <token>"
```

**Response `404`:**
```json
{
  "detail": "User not found"
}
```

---

### POST /users

Crear nuevo usuario (requiere rol `admin`).

```bash
curl -X POST http://localhost:8000/users \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "new@example.com",
    "password": "secret123"
  }'
```

**Response `201`:**
```json
{
  "id": 2,
  "username": "newuser",
  "email": "new@example.com",
  "is_active": true,
  "role": "user"
}
```

---

### PUT /users/{id}

Actualizar usuario.

```bash
curl -X PUT http://localhost:8000/users/1 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"email": "updated@example.com"}'
```

---

### DELETE /users/{id}

Eliminar usuario (requiere rol `admin`).

```bash
curl -X DELETE http://localhost:8000/users/1 \
  -H "Authorization: Bearer <token>"
```

**Response `204`:** No content

---

## Items

### GET /items

Listar items con paginación.

| Query Param | Type | Default | Description |
|-------------|------|---------|-------------|
| `skip` | int | 0 | Número de items a saltar |
| `limit` | int | 100 | Máximo número de items |

```bash
curl -X GET "http://localhost:8000/items?skip=0&limit=10" \
  -H "Authorization: Bearer <token>"
```

**Response `200`:**
```json
{
  "total": 50,
  "skip": 0,
  "limit": 10,
  "items": [
    {
      "id": 1,
      "name": "Item Name",
      "description": "Description here",
      "created_at": "2026-03-23T10:00:00Z"
    }
  ]
}
```

---

### POST /items

Crear item (requiere autenticación).

```bash
curl -X POST http://localhost:8000/items \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Item Name",
    "description": "Description here"
  }'
```

**Response `201`:**
```json
{
  "id": 1,
  "name": "Item Name",
  "description": "Description here",
  "created_at": "2026-03-23T10:00:00Z"
}
```

---

### GET /items/{id}

Obtener item por ID.

```bash
curl -X GET http://localhost:8000/items/1 \
  -H "Authorization: Bearer <token>"
```

---

### PUT /items/{id}

Actualizar item.

```bash
curl -X PUT http://localhost:8000/items/1 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Name"}'
```

---

### DELETE /items/{id}

Eliminar item.

```bash
curl -X DELETE http://localhost:8000/items/1 \
  -H "Authorization: Bearer <token>"
```

**Response `204`:** No content

---

## Health & Metrics

### GET /health

Health check simple.

```bash
curl http://localhost:8000/health
```

**Response `200`:**
```json
{
  "status": "healthy",
  "timestamp": "2026-03-23T10:00:00Z"
}
```

---

### GET /metrics

Métricas en formato Prometheus.

```bash
curl http://localhost:8000/metrics
```

---

## Error Responses

Todos los errores siguen este formato:

```json
{
  "detail": "Human-readable error message",
  "error_code": "VALIDATION_ERROR"
}
```

| Código HTTP | Significado | Ejemplo |
|-------------|-------------|---------|
| 400 | Bad Request | Parámetros inválidos |
| 401 | Unauthorized | Token faltante o expirado |
| 403 | Forbidden | Sin permisos para este recurso |
| 404 | Not Found | Recurso no encontrado |
| 422 | Unprocessable Entity | Validación de datos fallida |
| 429 | Too Many Requests | Rate limit excedido |
| 500 | Internal Server Error | Error interno del servidor |

**Rate Limit Error (429):**
```json
{
  "detail": "Rate limit exceeded. Please try again later.",
  "retry_after": 60
}
```

---

## Rate Limiting

| Tipo | Límite | Scope |
|------|--------|-------|
| Sin auth | 100 req/min | Por IP |
| Con auth | 1000 req/hour | Por usuario |

**Response headers:**
- `X-RateLimit-Limit` — Límite máximo
- `X-RateLimit-Remaining` — Requests restantes
- `X-RateLimit-Reset` — Timestamp de reseteo (Unix)
