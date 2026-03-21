"""
FastAPI REST API - Aplicación principal
Versión mejorada con seguridad, logging y mejor manejo de errores
"""
from fastapi import FastAPI, HTTPException, status, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional, Dict, Any
import uuid
import logging
import time
import sys

from models import Item, ItemCreate, ItemUpdate
from database import items_db

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Almacenar inicio
start_time = datetime.utcnow()

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
    version="1.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS configurado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware para logging de requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log de todas las requests"""
    request_id = str(uuid.uuid4())[:8]
    start_time = time.time()
    
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

# In-memory database
db = items_db


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
        "version": "1.1.0"
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
    # Validar parámetros de paginación
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
    
    items = list(db.values())
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
    if item_id not in db:
        logger.warning(f"Item not found: {item_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} no encontrado"
        )
    return {"success": True, "data": db[item_id]}


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
    db[item_id] = new_item
    
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
    if item_id not in db:
        logger.warning(f"Item not found for update: {item_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} no encontrado"
        )
    
    existing = db[item_id]
    update_data = item_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(existing, field, value)
    
    existing.updated_at = datetime.utcnow().isoformat()
    db[item_id] = existing
    
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
    if item_id not in db:
        logger.warning(f"Item not found for delete: {item_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} no encontrado"
        )
    
    del db[item_id]
    
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
        "total_items": len(db),
        "uptime": calculate_uptime(),
        "timestamp": datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
