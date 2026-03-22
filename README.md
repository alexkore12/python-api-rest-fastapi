# FastAPI REST API

REST API de alto rendimiento con Python FastAPI - **Versión 1.2.0 con Tests Completos**

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
- **Tests completos** - pytest con coverage

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

## 🧪 Testing

### Tests v1.2.0

```bash
# Instalar dependencias de test
pip install pytest pytest-asyncio httpx

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
| CRUD Operations | ✅ Create, Read, Update, Delete |
| Validation | ✅ Required fields, types, ranges |
| Pagination | ✅ skip/limit parameters |
| Statistics | ✅ Stats endpoint |

## 📁 Estructura del Proyecto

```
python-api-rest-fastapi/
├── main.py                 # Aplicación principal (v1.2.0)
├── models.py               # Modelos Pydantic
├── database.py             # Configuración de BD
├── requirements.txt        # Dependencias
├── Dockerfile              # Imagen Docker
├── docker-compose.yaml     # Orquestación
├── .dockerignore           # Exclusiones Docker
├── tests/
│   └── test_api.py        # Suite de tests
├── README.md               # Este archivo
└── .env.example           # Ejemplo de configuración
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

### v1.2.0 (2026-03-22)
- ✅ Suite completa de tests (tests/test_api.py)
- ✅ Tests de validación de entrada
- ✅ Tests de paginación
- ✅ Tests de estadísticas
- ✅ Coverage configurado

### v1.1.0 (2026-03-21)
- ✅ Middleware de logging estructurado
- ✅ Mejora en manejo de errores
- ✅ Validación de parámetros de paginación
- ✅ Headers de response (X-Request-ID, X-Process-Time)
- ✅ Documentación OpenAPI mejorada

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
