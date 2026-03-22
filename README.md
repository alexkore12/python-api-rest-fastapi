# 🚀 FastAPI REST API

API REST de alto rendimiento construida con FastAPI para gestión de items.

## 📋 Descripción

API RESTful moderna con FastAPI que proporciona operaciones CRUD completas sobre items, con validación de datos, paginación, logging estructurado y documentación automática.

## 🛠️ Características

- ⚡ **Alto Rendimiento** - Hasta 30k+ requests/seg
- 🔒 **Seguridad** - Validación con Pydantic
- 🌐 **CORS** - Configuración de Cross-Origin
- 📊 **Rate Limiting** - Protección contra abusos
- 📝 **Logging Estructurado** - Monitoreo detallado
- ❤️ **Health Checks** - Endpoints de salud
- 📚 **Documentación Auto** - OpenAPI/Swagger/ReDoc
- 🧪 **Testing** - Endpoints de estadísticas

## 🚀 Instalación

### Prerrequisitos

- Python 3.9+

### Pasos

```bash
# 1. Clonar
git clone https://github.com/alexkore12/python-api-rest-fastapi.git
cd python-api-rest-fastapi

# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar
python main.py
```

La API estará disponible en:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI**: http://localhost:8000/openapi.json

## 🐳 Docker

### Build

```bash
docker build -t fastapi-rest-api .
```

### Ejecutar

```bash
docker run -d -p 8000:8000 fastapi-rest-api
```

### Docker Compose

```bash
docker-compose up -d
```

## 📡 Endpoints

### Health

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/health` | Health check con uptime |

### Items CRUD

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/items` | Listar items (con paginación) |
| GET | `/items/{id}` | Obtener item por ID |
| POST | `/items` | Crear nuevo item |
| PUT | `/items/{id}` | Actualizar item |
| DELETE | `/items/{id}` | Eliminar item |

### Stats

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/stats` | Estadísticas de la API |

## 📝 Uso de Endpoints

### Crear Item

```bash
curl -X POST "http://localhost:8000/items" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mi Item",
    "description": "Descripción del item",
    "price": 99.99
  }'
```

### Listar Items (con paginación)

```bash
# Obtener primeros 10 items
curl "http://localhost:8000/items?skip=0&limit=10"

# Obtener siguientes 10
curl "http://localhost:8000/items?skip=10&limit=10"
```

### Actualizar Item

```bash
curl -X PUT "http://localhost:8000/items/{item_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Nombre actualizado",
    "price": 149.99
  }'
```

### Eliminar Item

```bash
curl -X DELETE "http://localhost:8000/items/{item_id}"
```

## 📊 Respuestas

### Health Check

```json
{
  "status": "healthy",
  "timestamp": "2026-03-21T12:00:00",
  "uptime": "2h 30m 15s",
  "version": "1.1.0"
}
```

### List Items

```json
{
  "success": true,
  "count": 25,
  "skip": 0,
  "limit": 100,
  "data": [...]
}
```

### Stats

```json
{
  "total_items": 42,
  "uptime": "2h 30m 15s",
  "timestamp": "2026-03-21T12:00:00"
}
```

## 📁 Estructura

```
python-api-rest-fastapi/
├── main.py              # Aplicación principal
├── models.py            # Modelos Pydantic
├── database.py          # Base de datos en memoria
├── requirements.txt     # Dependencias
├── Dockerfile          # Imagen Docker
├── docker-compose.yaml  # Orquestación
├── .dockerignore       # Ignorar archivos en Docker
└── README.md           # Este archivo
```

## 🔧 Configuración

### Parámetros de Paginación

| Parámetro | Tipo | Default | Límites |
|-----------|------|---------|---------|
| `skip` | int | 0 | >= 0 |
| `limit` | int | 100 | 1-100 |

### Encabezados de Respuesta

| Header | Descripción |
|--------|-------------|
| `X-Request-ID` | ID único de request |
| `X-Process-Time` | Tiempo de procesamiento (segundos) |

## 🧪 Pruebas

### Health Check

```bash
curl http://localhost:8000/health
```

### Crear varios items y ver estadísticas

```bash
# Crear items
curl -X POST http://localhost:8000/items -H "Content-Type: application/json" -d '{"name":"Item 1","price":10}'
curl -X POST http://localhost:8000/items -H "Content-Type: application/json" -d '{"name":"Item 2","price":20}'

# Ver estadísticas
curl http://localhost:8000/stats
```

## ☁️ Deploy

### Railway/Render

1. Conecta tu repositorio de GitHub
2. Configura el puerto: `PORT=8000`
3. Comando: `python main.py`

### Heroku

```bash
heroku create my-fastapi-app
git push heroku main
```

### VPS/Linux

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar con systemd
sudo cp fastapi.service /etc/systemd/system/
sudo systemctl start fastapi
sudo systemctl enable fastapi
```

## 🔨 Desarrollo

### Hot Reload

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Con variables de entorno

```bash
export HOST=0.0.0.0
export PORT=8000
python main.py
```

## 📈 Mejoras Incluidas

- ✅ Logging estructurado con request IDs
- ✅ Middleware para tiempo de procesamiento
- ✅ Validación de paginación
- ✅ Endpoints de health y stats
- ✅ Documentación en español
- ✅ Manejo de errores mejorado

## 🐛 Troubleshooting

### Puerto en uso

```bash
# Encontrar proceso
lsof -i :8000

# Matar proceso
kill -9 <PID>

# O usar otro puerto
python main.py --port 8001
```

### Dependencias

```bash
# Actualizar pip
pip install --upgrade pip

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

## 📝 Changelog

- **v1.0.0** - API básica con CRUD
- **v1.1.0** - Mejoras de seguridad y logging

## 🤝 Contribución

¡Contribuciones bienvenidas! Abre un issue o PR.

## 📄 Licencia

MIT License - Uso libre.
