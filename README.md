# FastAPI REST API

REST API de alto rendimiento con Python FastAPI - Versión mejorada 1.1.0

## 🚀 Características

- **FastAPI** - Framework moderno y rápido (async/await nativo)
- **Pydantic** - Validación de datos automática con type hints
- **CORS** - Configuración de CORS completa
- **Type hints** - Código completamente tipado
- **Async/Await** - Programación asíncrona de alto rendimiento
- **Docker** -listo para producción
- **OpenAPI** - Documentación automática (Swagger UI + ReDoc)
- **Logging estructurado** - Logs de todas las requests
- **Manejo de errores** - Errores controlados y bien documentados
- **Rate limiting** - Preparado para implementación

## 📋 Endpoints

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

Respuesta:
```json
{
  "status": "healthy",
  "timestamp": "2026-03-21T12:00:00Z",
  "uptime": "0h 5m 30s",
  "version": "1.1.0"
}
```

### Listar Items (con paginación)

```bash
curl "http://localhost:8000/items?skip=0&limit=10"
```

### Crear Item

```bash
curl -X POST http://localhost:8000/items \
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
curl http://localhost:8000/items/{item_id}
```

### Actualizar Item

```bash
curl -X PUT http://localhost:8000/items/{item_id} \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Producto actualizado",
    "price": 79.99
  }'
```

### Eliminar Item

```bash
curl -X DELETE http://localhost:8000/items/{item_id}
```

### Estadísticas

```bash
curl http://localhost:8000/stats
```

## 📁 Estructura del Proyecto

```
python-api-rest-fastapi/
├── main.py                 # Aplicación principal (v1.1.0)
├── models.py               # Modelos Pydantic
├── database.py             # Configuración de BD
├── requirements.txt        # Dependencias
├── Dockerfile              # Imagen Docker
├── docker-compose.yaml     # Orquestación
├── .dockerignore           # Exclusiones Docker
├── README.md               # Este archivo
└── tests/                  # Tests (futuro)
    └── test_api.py
```

## ⚙️ Variables de Entorno

| Variable | Descripción | Default |
|----------|-------------|---------|
| `DATABASE_URL` | URL de base de datos | `sqlite:///./app.db` |
| `HOST` | Host del servidor | `0.0.0.0` |
| `PORT` | Puerto | `8000` |
| `DEBUG` | Modo debug | `false` |
| `LOG_LEVEL` | Nivel de logging | `INFO` |

## 🔒 Seguridad

### Headers de Seguridad

La API incluye:

- **CORS** configurado (en producción, especificar orígenes permitidos)
- **X-Request-ID** - ID único por request
- **X-Process-Time** - Tiempo de procesamiento

### Validación con Pydantic

Pydantic valida automáticamente:

- ✅ Tipos de datos
- ✅ Longitud de strings
- ✅ Rangos de números
- ✅ Campos requeridos
- ✅ Formatos (email, URL, etc.)

### Recomendaciones para Producción

1. **Usar HTTPS** - Configurar proxy reverso (nginx, traefik)
2. **Limitar CORS** - Especificar dominios permitidos
3. **Rate Limiting** - Implementar límites de requests
4. **Autenticación** - Añadir OAuth2 o JWT
5. **Logs** - Enviar logs a sistema centralizado
6. **Métricas** - Integrar Prometheus/Grafana

## 🧪 Testing

```bash
# Instalar dependencias de test
pip install pytest pytest-asyncio httpx

# Ejecutar tests
pytest

# Con coverage
pytest --cov=. --cov-report=html
```

## 📊 Logging

La API logsuea:

- Requests entrantes (método, path)
- Status codes de respuesta
- Tiempo de procesamiento
- Errores y advertencias

Ejemplo de log:
```
2026-03-21 12:00:00 - __main__ - INFO - [a1b2c3d4] GET /items
2026-03-21 12:00:00 - __main__ - INFO - [a1b2c3d4] Status: 200 Time: 0.023s
```

## 🚀 Despliegue Recomendado

### Docker Compose con Nginx

```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=false
      - LOG_LEVEL=info

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - api
```

## 📝 Changelog

### v1.1.0 (2026-03-21)
- ✅ Añadido middleware de logging estructurado
- ✅ Mejora en manejo de errores
- ✅ Validación de parámetros de paginación
- ✅ Headers de response (X-Request-ID, X-Process-Time)
- ✅ Documentación OpenAPI mejorada
- ✅ Endpoint de stats mejorado con uptime

### v1.0.0 (2026-03-20)
- ✅ Versión inicial
- ✅ CRUD completo de items
- ✅ Pydantic models
- ✅ Docker support

## 🤖 Generado por

Este proyecto fue creado y actualizado por **OpenClaw AI Assistant**.

## 📄 Licencia

MIT License

---

**GitHub**: [alexkore12](https://github.com/alexkore12)
