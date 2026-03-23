# FastAPI REST API

REST API de alto rendimiento con Python FastAPI - Versión 1.3.0 con Tests Completos y CI/CD

## Características

- **FastAPI** - Framework moderno y rápido (async/await nativo)
- **Pydantic** - Validación de datos automática con type hints
- **CORS** - Configuración de CORS completa
- **Type hints** - Código completamente tipado
- **Async/Await** - Programación asíncrona de alto rendimiento
- **Docker** - Listo para producción
- **OpenAPI** - Documentación automática (Swagger UI + ReDoc)
- **Logging estructurado** - Logs de todas las requests
- **Manejo de errores** - Errores controlados y bien documentados
- **Tests completos** - pytest con coverage
- **CI/CD** - GitHub Actions integrado

## Instalación

```bash
# Clonar repositorio
git clone https://github.com/alexkore12/python-api-rest-fastapi.git
cd python-api-rest-fastapi

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate    # Windows

# Instalar dependencias
pip install -r requirements.txt
```

## Uso

### Desarrollo

```bash
# Con hot reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# O directamente
python main.py
```

### Producción

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Docker

```bash
# Build
docker build -t fastapi-app .

# Run
docker run -p 8000:8000 fastapi-app

# Docker Compose
docker-compose up -d
```

## Documentación Automática

Una vez ejecutando la API:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **OpenAPI JSON**: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

## Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/items` | Listar items (paginado) |
| GET | `/items/{id}` | Obtener item por ID |
| POST | `/items` | Crear nuevo item |
| PUT | `/items/{id}` | Actualizar item |
| DELETE | `/items/{id}` | Eliminar item |
| GET | `/stats` | Estadísticas |

## Ejemplos de Uso

### Health Check

```bash
curl http://localhost:8000/health
```

### Listar Items (Paginado)

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

## Configuración

### Variables de Entorno

| Variable | Descripción | Default |
|----------|-------------|---------|
| `DATABASE_URL` | URL de base de datos | `sqlite:///./app.db` |
| `HOST` | Host del servidor | `0.0.0.0` |
| `PORT` | Puerto | `8000` |
| `DEBUG` | Modo debug | `false` |
| `LOG_LEVEL` | Nivel de logging | `INFO` |

## Estructura del Proyecto

```
python-api-rest-fastapi/
├── main.py                  # Aplicación principal (v1.3.0)
├── models.py                # Modelos Pydantic
├── database.py              # Configuración de BD
├── requirements.txt        # Dependencias
├── Dockerfile               # Imagen Docker
├── docker-compose.yaml      # Orquestación
├── .dockerignore            # Exclusiones Docker
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions CI/CD
├── tests/
│   └── test_api.py          # Suite de tests
├── README.md                # Este archivo
└── .env.example             # Ejemplo de configuración
```

## Tests

###安装依赖

```bash
pip install pytest pytest-asyncio httpx
```

###Ejecutar tests

```bash
pytest tests/ -v
```

###Con coverage

```bash
pytest tests/ --cov=. --cov-report=html
```

###Coverage en terminal

```bash
pytest tests/ --cov=. --cov-report=term-missing
```

###Cobertura de Tests

| Categoría | Tests |
|-----------|-------|
| Health Check | ✅ Status, uptime |
| CRUD Operations | ✅ Create, Read, Update, Delete |
| Validation | ✅ Required fields, types, ranges |
| Pagination | ✅ skip/limit parameters |
| Statistics | ✅ Stats endpoint |

## Validación con Pydantic

Pydantic valida automáticamente:

- ✅ Tipos de datos
- ✅ Longitud de strings
- ✅ Rangos de números
- ✅ Campos requeridos
- ✅ Formatos (email, URL, etc.)

## Headers de Respuesta

La API incluye:

- CORS configurado (en producción, especificar orígenes permitidos)
- X-Request-ID - ID único por request
- X-Process-Time - Tiempo de procesamiento

## Seguridad en Producción

- Usar HTTPS - Configurar proxy reverso (nginx, traefik)
- Limitar CORS - Especificar dominios permitidos
- Rate Limiting - Implementar límites de requests
- Autenticación - Añadir OAuth2 o JWT
- Logs - Enviar logs a sistema centralizado
- Métricas - Integrar Prometheus/Grafana

## Docker Compose con Nginx

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

## GitHub Actions CI/CD

El proyecto incluye workflow automático:

```yaml
name: CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest tests/ -v
```

## Changelog

- ✅ v1.3.0 - GitHub Actions CI/CD añadido
- ✅ v1.2.0 - Suite completa de tests
- ✅ v1.1.0 - Middleware de logging estructurado
- ✅ v1.0.0 - Versión inicial

## Dependencias

- FastAPI
- Pydantic
- Uvicorn
- SQLAlchemy (optional)
- pytest

## Licencia

MIT

## Autor

GitHub: [alexkore12](https://github.com/alexkore12)

Este proyecto fue creado y actualizado por OpenClaw AI Assistant.
