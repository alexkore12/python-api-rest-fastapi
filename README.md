# Python FastAPI REST API

REST API de alto rendimiento con Python FastAPI.

## 🎯 Características

- **FastAPI** - Framework moderno y rápido
- **Pydantic** - Validación de datos automática
- **SQLAlchemy** - ORM para base de datos
- **Async/Await** - Programación asíncrona
- **Docker** - Listo para producción
- **OpenAPI** - Documentación automática
- **JWT Auth** - Autenticación
- **Pytest** - Testing integrado

## 🚀 Inicio Rápido

### Instalación Local

```bash
# Clonar
git clone https://github.com/alexkore12/python-api-rest-fastapi.git
cd python-api-rest-fastapi

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
uvicorn main:app --reload
```

### Con Docker

```bash
# Build
docker build -t fastapi-app .

# Run
docker run -p 8000:8000 fastapi-app
```

### Con Docker Compose

```bash
docker-compose up -d
```

## 📡 Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | /health | Health check |
| GET | /items | Listar items |
| GET | /items/{id} | Obtener item |
| POST | /items | Crear item |
| PUT | /items/{id} | Actualizar item |
| DELETE | /items/{id} | Eliminar item |
| GET | /stats | Estadísticas |

## 📖 Documentación API

Accede a:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 💻 Ejemplos

```bash
# Health check
curl http://localhost:8000/health

# Listar items
curl http://localhost:8000/items

# Crear item
curl -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Nuevo producto", "price": 49.99}'

# Obtener item
curl http://localhost:8000/items/1

# Actualizar item
curl -X PUT http://localhost:8000/items/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Producto actualizado", "price": 79.99}'

# Eliminar item
curl -X DELETE http://localhost:8000/items/1
```

## 📂 Estructura

```
python-api-rest-fastapi/
├── main.py              # Aplicación principal
├── models.py            # Modelos Pydantic
├── database.py         # Configuración de BD
├── requirements.txt    # Dependencias
├── Dockerfile          # Imagen Docker
├── docker-compose.yaml # Orquestación
├── .dockerignore       # Exclusiones Docker
├── alembic/            # Migraciones
├── tests/              # Tests
└── README.md           # Este archivo
```

## ⚙️ Variables de Entorno

| Variable | Descripción | Default |
|----------|-------------|---------|
| DATABASE_URL | URL de base de datos | sqlite:///./app.db |
| HOST | Host del servidor | 0.0.0.0 |
| PORT | Puerto | 8000 |
| DEBUG | Modo debug | false |
| SECRET_KEY | Clave secreta JWT | - |
| ALGORITHM | Algoritmo JWT | HS256 |
| ACCESS_TOKEN_EXPIRE | Expiración token | 30 |

## 🛡️ Seguridad

### Autenticación JWT

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username
```

### Validación

Pydantic valida automáticamente:
- Tipos de datos
- Longitud de strings
- Rangos de números
- Campos requeridos
- Formatos (email, URL, etc.)

```python
from pydantic import BaseModel, Field, EmailStr

class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    description: str | None = Field(None, max_length=500)
    email: EmailStr | None = None
```

## 🧪 Testing

### Tests con Pytest

```bash
# Instalar dependencias de test
pip install pytest pytest-asyncio httpx

# Ejecutar tests
pytest

# Con coverage
pytest --cov=main --cov-report=html
```

### Ejemplo de Test

```python
from fastapi.testclient import TestClient

def test_read_items():
    response = client.get("/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

## 🐳 Docker

### Optimizaciones

```dockerfile
# Multi-stage build para producción
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

COPY . .
USER 1000

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

### Docker Compose con PostgreSQL

```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/appdb
    depends_on:
      - db

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=appdb
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

## 📊 Base de Datos

### Modelos SQLAlchemy

```python
from sqlalchemy import Column, Integer, String, Float
from database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    description = Column(String, nullable=True)
```

### Migraciones Alembic

```bash
# Generar migración
alembic revision --autogenerate -m "Add items table"

# Aplicar migraciones
alembic upgrade head

# Rollback
alembic downgrade -1
```

## 🚀 Despliegue

### Producción con Gunicorn

```bash
# Instalar
pip install gunicorn

# Ejecutar workers
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Environment Variables

```bash
# Production
export DATABASE_URL="postgresql://user:pass@host/db"
export SECRET_KEY="your-secret-key"
export DEBUG=false
```

## 📈 Métricas

### Health Check

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "uptime": time.time() - START_TIME,
        "version": "1.0.0"
    }
```

### Prometheus Metrics

```bash
pip install prometheus-client
```

```python
from prometheus_client import Counter, generate_latest

REQUEST_COUNT = Counter('requests_total', 'Total requests')

@app.get("/metrics")
async def metrics():
    return generate_latest()
```

## 🤖 Generado Automáticamente

Este proyecto fue creado y actualizado por OpenClaw AI Assistant.

## 📝 Licencia

MIT License

## 👤 Autor

- **GitHub**: [alexkore12](https://github.com/alexkore12)
