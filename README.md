# Python FastAPI REST API

REST API de alto rendimiento con Python FastAPI.

## 🎯 Características

- **FastAPI** - Framework moderno y rápido
- **Pydantic** - Validación de datos automática
- **CORS** - Configuración de CORS completa
- **Type hints** - Código tipado
- **Async/Await** - Programación asíncrona
- **Docker** -listo para producción
- **OpenAPI** - Documentación automática

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
├── database.py          # Configuración de BD
├── requirements.txt     # Dependencias
├── Dockerfile          # Imagen Docker
├── docker-compose.yaml # Orquestación
├── .dockerignore       # Exclusiones Docker
└── README.md           # Este archivo
```

## ⚙️ Variables de Entorno

| Variable | Descripción | Default |
|----------|-------------|---------|
| DATABASE_URL | URL de base de datos | sqlite:///./app.db |
| HOST | Host del servidor | 0.0.0.0 |
| PORT | Puerto | 8000 |
| DEBUG | Modo debug | false |

## ✅ Validación

Pydantic valida automáticamente:
- Tipos de datos
- Longitud de strings
- Rangos de números
- Campos requeridos
- Formatos (email, URL, etc.)

## 🔒 Seguridad

- CORS configurado
- Validación de input
- Type hints completos
- Error handling apropiado

## 🧪 Testing

```bash
# Instalar dependencias de test
pip install pytest pytest-asyncio httpx

# Ejecutar tests
pytest
```

## 🤖 Generado Automáticamente

Este proyecto fue creado y actualizado por OpenClaw AI Assistant.

## 📝 Licencia

MIT License

## 👤 Autor

- **GitHub**: [alexkore12](https://github.com/alexkore12)
