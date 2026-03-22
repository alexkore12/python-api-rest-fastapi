# FastAPI REST API

REST API de alto rendimiento con Python FastAPI - **Versión 2.1 con Rate Limiting**

## 🚀 Características

- **FastAPI** - Framework moderno y rápido (async/await nativo)
- **Pydantic** - Validación de datos automática con type hints
- **JWT Authentication** - Seguridad con tokens JWT
- **OAuth2** - Flujo de autenticación estándar
- **Rate Limiting** - Límite de requests (100/min público, 60/min autenticado)
- **CORS** - Configuración de CORS completa
- **Type hints** - Código completamente tipado
- **Async/Await** - Programación asíncrona de alto rendimiento
- **Docker** -listo para producción
- **OpenAPI** - Documentación automática (Swagger UI + ReDoc)
- **Logging estructurado** - Logs de todas las requests
- **Manejo de errores** - Errores controlados y bien documentados
- **Tests completos** - pytest con coverage

## 📋 Endpoints

### Autenticación

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/token` | Obtener token JWT |
| GET | `/auth/me` | Usuario actual |

### Items (Protegidos)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/items` | Listar items (paginado) |
| GET | `/items/{id}` | Obtener item por ID |
| POST | `/items` | Crear nuevo item |
| PUT | `/items/{id}` | Actualizar item |
| DELETE | `/items/{id}` | Eliminar item |
| GET | `/stats` | Estadísticas |

## 🛠️ Instalación

```bash
# Clonar repositorio
git clone https://github.com/alexkore12/python-api-rest-fastapi.git
cd python-api-rest-fastapi

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
```

## ▶️ Ejecución

### Desarrollo

```bash
# Con hot reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# O directamente
python main.py
```

### Docker

```bash
# Build
docker build -t fastapi-app .

# Run
docker run -p 8000:8000 fastapi-app

# Docker Compose
docker-compose up -d
```

## 🔐 Autenticación

### Obtener Token

```bash
curl -X POST http://localhost:8000/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

Respuesta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Usar Token

```bash
curl http://localhost:8000/items \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Usuarios de Demo

| Username | Password | Rol |
|----------|----------|-----|
| admin | admin123 | admin |
| user | password | user |

## 📖 Documentación

Una vez ejecutando la API:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **OpenAPI JSON**: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

## 🔧 Uso de la API

### Health Check

```bash
curl http://localhost:8000/health
```

### Autenticarse

```bash
curl -X POST http://localhost:8000/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

### Listar Items (protegido)

```bash
curl "http://localhost:8000/items?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Crear Item

```bash
curl -X POST http://localhost:8000/items \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Nuevo producto",
    "description": "Descripción del producto",
    "price": 49.99,
    "in_stock": true
  }'
```

### Obtener Item

```bash
curl http://localhost:8000/items/{item_id} \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Actualizar Item

```bash
curl -X PUT http://localhost:8000/items/{item_id} \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Producto actualizado",
    "price": 79.99
  }'
```

### Eliminar Item

```bash
curl -X DELETE http://localhost:8000/items/{item_id} \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Estadísticas

```bash
curl http://localhost:8000/stats \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🧪 Testing

```bash
# Instalar dependencias de test
pip install pytest pytest-asyncio httpx python-jose

# Ejecutar tests
pytest tests/ -v

# Con coverage
pytest tests/ --cov=. --cov-report=html

# Coverage en terminal
pytest tests/ --cov=. --cov-report=term-missing
```

### Cobertura de Tests

| Categoría | Tests |
|-----------|-------|
| Health Check | ✅ Status, uptime |
| Autenticación | ✅ Login, token validation |
| CRUD Operations | ✅ Create, Read, Update, Delete |
| Validation | ✅ Required fields, types, ranges |
| Pagination | ✅ skip/limit parameters |
| Statistics | ✅ Stats endpoint |

## ⚙️ Configuración

### Variables de Entorno

| Variable | Descripción | Default |
|----------|-------------|---------|
| `DATABASE_URL` | URL de base de datos | sqlite:///./app.db |
| `HOST` | Host del servidor | 0.0.0.0 |
| `PORT` | Puerto | 8000 |
| `DEBUG` | Modo debug | false |
| `LOG_LEVEL` | Nivel de logging | INFO |
| `SECRET_KEY` | Clave JWT | (configurable) |

## 🛡️ Seguridad

La API incluye:

- **JWT Tokens** - Autenticación stateless
- **OAuth2 Password Flow** - Flujo estándar de autenticación
- **CORS configurado** - En producción, especificar orígenes permitidos
- **Rate Limiting** - Límite de requests para prevenir abuse
- **X-Request-ID** - ID único por request
- **X-Process-Time** - Tiempo de procesamiento
- **Pydantic Validation** - Validación automática de entrada

### Recomendaciones de Producción

- Usar HTTPS - Configurar proxy reverso (nginx, traefik)
- Limitar CORS - Especificar dominios permitidos
- Rate Limiting - Implementar límites de requests
- Autenticación JWT ya incluida ✅
- Logs - Enviar logs a sistema centralizado
- Métricas - Integrar Prometheus/Grafana

## 📁 Estructura del Proyecto

```
python-api-rest-fastapi/
├── main.py              # Aplicación principal (v2.0)
├── auth.py              # Módulo de autenticación JWT
├── models.py            # Modelos Pydantic
├── database.py          # Configuración de BD
├── requirements.txt    # Dependencias
├── Dockerfile           # Imagen Docker
├── docker-compose.yaml  # Orquestación
├── .dockerignore        # Exclusiones Docker
├── tests/
│   └── test_api.py     # Suite de tests
├── README.md            # Este archivo
└── .env.example        # Ejemplo de configuración
```

## 📝 Changelog

### v2.1.0 (2026-03-22)
- ✅ Rate Limiting con slowapi (100 req/min público, 60 req/min autenticado)
- ✅ Manejo de errores de rate limit (HTTP 429)
- ✅ Documentación de rate limiting

### v2.0.0 (2026-03-22)
- ✅ Autenticación JWT completa
- ✅ OAuth2 Password Flow
- ✅ Endpoints protegidos
- ✅ Módulo auth.py separado
- ✅ Tests de autenticación

### v1.2.0 (2026-03-21)
- ✅ Tests completos
- ✅ Logging estructurado
- ✅ Validación mejorada

### v1.1.0 (2026-03-20)
- ✅ Middleware de logging
- ✅ Mejora en manejo de errores

### v1.0.0 (2026-03-19)
- ✅ CRUD completo de items
- ✅ Pydantic models
- ✅ Docker support

## 📄 Licencia

MIT License

GitHub: [alexkore12](https://github.com/alexkore12)

## 🤖 Actualizado por

OpenClaw AI Assistant - 2026-03-22
*Mejoras v2.0: Autenticación JWT, OAuth2, seguridad mejorada*
