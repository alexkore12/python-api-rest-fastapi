# 🚀 Python REST API (FastAPI)

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)
[![Security: Grype](https://img.shields.io/badge/Security-Grype-orange.svg)](.grype.yaml)

## 📋 Descripción

API REST moderna construida con FastAPI, diseñada para ser rápida, segura y fácil de mantener.

## ✨ Características

- ⚡ **Alto Rendimiento**: Gracias a FastAPI y Uvicorn
- 🔒 **Seguridad**: Autenticación JWT, CORS, rate limiting
- 📝 **API Documentation**: Swagger UI automático
- 🐳 **Docker Ready**: Despliegue fácil con Docker
- 🔍 **Security Scanning**: Escaneo automático con Grype
- ✅ **Pre-commit Hooks**: Code quality checks
- 📊 **Logging Estructurado**: Con correlation IDs

## 🚀 Instalación

### Prerequisites
- Python 3.11+
- Docker (opcional)

### Instalación Local

```bash
# Clonar el repositorio
git clone https://github.com/alexkore12/python-api-rest-fastapi.git
cd python-api-rest-fastapi

# Crear entorno virtual
python -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env

# Ejecutar servidor de desarrollo
uvicorn main:app --reload
```

### Con Docker

```bash
# Construir imagen
docker build -t python-api-rest-fastapi .

# Ejecutar
docker run -p 8000:8000 --env-file .env python-api-rest-fastapi
```

### Con Docker Compose

```bash
docker-compose up -d
```

## ⚙️ Configuración

| Variable | Descripción | Default |
|----------|-------------|---------|
| `APP_NAME` | Nombre de la aplicación | FastAPI |
| `APP_VERSION` | Versión de la API | 1.0.0 |
| `DEBUG` | Modo debug | false |
| `DATABASE_URL` | URL de base de datos | sqlite:///./api.db |
| `SECRET_KEY` | Clave secreta para JWT | - |
| `ALGORITHM` | Algoritmo JWT | HS256 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Expiración del token | 30 |

## 📖 Documentación API

Una vez ejecutando, visita:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🏗️ Estructura del Proyecto

```
python-api-rest-fastapi/
├── .dockerignore
├── .env.example
├── .github/workflows/ci.yml
├── .gitignore
├── .grype.yaml
├── .pre-commit-config.yaml
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── Dockerfile
├── README.md
├── SECURITY.md
├── docker-compose.yaml
├── logging_utils.py
├── main.py
└── requirements.txt
```

## 🔒 Seguridad

- ✅ Escaneo con Grype en cada push
- ✅ Pre-commit hooks para code quality
- ✅ Autenticación JWT
- ✅ CORS configurado
- ✅ Rate limiting

Consulta [SECURITY.md](SECURITY.md) para reporte de vulnerabilidades.

## 🤝 Contribuir

Lee [CONTRIBUTING.md](CONTRIBUTING.md) antes de contribuir.

## 📝 Licencia

MIT License - veja [LICENSE](LICENSE) para detalhes.

## 👤 Autor

- **Alex** - [@alexkore12](https://github.com/alexkore12)
