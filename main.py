"""
FastAPI REST API - Aplicación principal
Versión mejorada con seguridad, logging y mejor manejo de errores
"""
import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict, Optional
import uuid
import logging
import time
import sys

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()

from models import Item, ItemCreate, ItemUpdate
from database import items_db

# Configurar logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Configuración
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# Rate limiting simple
rate_limit_store: Dict[str, list] = {}
RATE_LIMIT = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
RATE_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "60"))

# Almacenar inicio
start_time = datetime.utcnow()


def check_rate_limit(client_id: str) -> bool:
    """Verifica si el cliente excedió el rate limit"""
    now = time.time()
    if client_id not in rate_limit_store:
        rate_limit_store[client_id] = []
    
    # Limpiar requests antiguos
    rate_limit_store[client_id] = [
        req_time for req_time in rate_limit_store[client_id]
        if now - req_time < RATE_WINDOW
    ]
    
    if len(rate_limit_store[client_id]) >= RATE_LIMIT:
        return False
    
    rate_limit_store[client_id].append(now)
    return True


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager"""
    logger.info("🚀 Starting FastAPI REST API...")
    logger.info(f"📚 API Documentation: /docs")
    yield
    logger.info("🛑 Shutting down API...")


app = FastAPI(
    title="FastAPI REST API",
    description="""RESTful API de alto rendimiento con FastAPI.
    
## Características
- ✅ Validación con Pydantic
- ✅ CORS configurado
- ✅ Rate Limiting
- ✅ Logging estructurado
- ✅ Health checks
- ✅ Documentación OpenAPI""",
    version="1.2.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS configurado
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware para logging de requests y rate limiting
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log de todas las requests con rate limiting"""
    client_id = request.client.host if request.client else "unknown"
    request_id = str(uuid.uuid4())[:8]
    start_time = time.time()
    
    # Check rate limit
    if not check_rate_limit(client_id):
        logger.warning(f"[{request_id}] Rate limit exceeded for {client_id}")
        return JSONResponse(
            status_code=429,
            content={
                "success": False,
                "error": "Rate limit exceeded",
                "retry_after": RATE_WINDOW
            }
        )
    
    logger.info(f"[{request_id}] {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        logger.info(
            f"[{request_id}] Status: {response.status_code} "
            f"Time: {process_time:.3f}s"
        )
        
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.3f}"
        
        return response
        
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(
            f"[{request_id}] Error: {str(e)} "
            f"Time: {process_time:.3f}s"
        )
        raise


def calculate_uptime() -> str:
    """Calcular uptime desde el inicio"""
    delta = datetime.utcnow() - start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m {seconds}s"


# Health check
@app.get(
    "/health",
    summary="Health Check",
    description="Verificar estado de la API",
    tags=["Health"]
)
async def health_check():
    """Endpoint de health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime": calculate_uptime(),
        "version": "1.2.0"
    }


# GET all items
@app.get(
    "/items",
    status_code=status.HTTP_200_OK,
    summary="Listar Items",
    description="Obtener lista de todos los items con paginación",
    tags=["Items"],
    response_model=Dict[str, Any]
)
async def get_items(skip: int = 0, limit: int = 100):
    """Obtener lista de items"""
    if skip < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="skip debe ser >= 0"
        )
    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="limit debe estar entre 1 y 100"
        )
    
    items = list(items_db.values())
    total = len(items)
    
    logger.info(f"Fetching items: skip={skip}, limit={limit}, total={total}")
    
    return {
        "success": True,
        "count": total,
        "skip": skip,
        "limit": limit,
        "data": items[skip:skip+limit]
    }


# GET single item
@app.get(
    "/items/{item_id}",
    summary="Obtener Item",
    description="Obtener un item específico por su ID",
    tags=["Items"],
    response_model=Dict[str, Any]
)
async def get_item(item_id: str):
    """Obtener item por ID"""
    if item_id not in items_db:
        logger.warning(f"Item not found: {item_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} no encontrado"
        )
    return {"success": True, "data": items_db[item_id]}


# POST create item
@app.post(
    "/items",
    status_code=status.HTTP_201_CREATED,
    summary="Crear Item",
    description="Crear un nuevo item en la base de datos",
    tags=["Items"],
    response_model=Dict[str, Any]
)
async def create_item(item: ItemCreate):
    """Crear nuevo item"""
    item_id = str(uuid.uuid4())
    new_item = Item(
        id=item_id,
        **item.model_dump(),
        created_at=datetime.utcnow().isoformat()
    )
    items_db[item_id] = new_item
    
    logger.info(f"Created item: {item_id}")
    
    return {"success": True, "data": new_item}


# PUT update item
@app.put(
    "/items/{item_id}",
    summary="Actualizar Item",
    description="Actualizar un item existente",
    tags=["Items"],
    response_model=Dict[str, Any]
)
async def update_item(item_id: str, item_update: ItemUpdate):
    """Actualizar item existente"""
    if item_id not in items_db:
        logger.warning(f"Item not found for update: {item_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} no encontrado"
        )
    
    existing = items_db[item_id]
    update_data = item_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(existing, field, value)
    
    existing.updated_at = datetime.utcnow().isoformat()
    items_db[item_id] = existing
    
    logger.info(f"Updated item: {item_id}")
    
    return {"success": True, "data": existing}


# DELETE item
@app.delete(
    "/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar Item",
    description="Eliminar un item por su ID",
    tags=["Items"]
)
async def delete_item(item_id: str):
    """Eliminar item"""
    if item_id not in items_db:
        logger.warning(f"Item not found for delete: {item_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} no encontrado"
        )
    
    del items_db[item_id]
    
    logger.info(f"Deleted item: {item_id}")
    
    return None


# Stats endpoint
@app.get(
    "/stats",
    summary="Estadísticas",
    description="Obtener estadísticas de uso de la API",
    tags=["Stats"],
    response_model=Dict[str, Any]
)
async def get_stats():
    """Estadísticas de la API"""
    return {
        "total_items": len(items_db),
        "uptime": calculate_uptime(),
        "timestamp": datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        log_level=LOG_LEVEL.lower()
    )
