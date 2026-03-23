"""
FastAPI REST API - Aplicación principal
Versión 2.1 con Rate Limiting, Autenticación JWT y seguridad mejorada
"""
from fastapi import FastAPI, HTTPException, status, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import uuid
import logging
import time
import sys
import os

from models import Item, ItemCreate, ItemUpdate
from database import items_db
from security_headers import SecurityHeadersMiddleware
from auth import (
    create_access_token, 
    authenticate_user, 
    get_current_active_user,
    User,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

# Rate Limiter setup
limiter = Limiter(key_func=get_remote_address)

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
    logger.info("🚀 Starting FastAPI REST API v2.1...")
    logger.info(f"📚 API Documentation: /docs")
    logger.info(f"🔐 Authentication: JWT enabled")
    yield
    logger.info("🛑 Shutting down API...")

app = FastAPI(
    title="FastAPI REST API",
    description="""RESTful API de alto rendimiento con FastAPI.
    
## Características
- ✅ Validación con Pydantic
- ✅ Autenticación JWT
- ✅ CORS configurado
- ✅ Rate Limiting (100 req/min)
- ✅ Logging estructurado
- ✅ Health checks
- ✅ Documentación OpenAPI""",
    version="2.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add rate limiter to app state
app.state.limiter = limiter

# Rate limit handler
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "error": "Too Many Requests",
            "detail": "Rate limit exceeded. Please try again later.",
            "retry_after": exc.detail
        }
    )

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# CORS configurado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security headers middleware
app.add_middleware(SecurityHeadersMiddleware)

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


# ============================================
# ENDPOINTS DE AUTENTICACIÓN
# ============================================

@app.post(
    "/token",
    summary="Obtener Token",
    description="Autenticarse y obtener token JWT",
    tags=["Auth"]
)
@limiter.limit("10/minute")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    """Login para obtener token JWT"""
    user = authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@app.get(
    "/auth/me",
    summary="Usuario Actual",
    description="Obtener información del usuario autenticado",
    tags=["Auth"],
    response_model=Dict[str, Any]
)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Obtener usuario actual"""
    return {
        "username": current_user.username,
        "disabled": current_user.disabled
    }


# Health check (público) - 30 requests per minute
@app.get(
    "/health",
    summary="Health Check",
    description="Verificar estado de la API",
    tags=["Health"]
)
@limiter.limit("30/minute")
async def health_check(request: Request):
    """Endpoint de health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime": calculate_uptime(),
        "version": "2.0.0"
    }


# GET all items (protegido) - 60 requests per minute
@app.get(
    "/items",
    status_code=status.HTTP_200_OK,
    summary="Listar Items",
    description="Obtener lista de todos los items con paginación",
    tags=["Items"],
    response_model=Dict[str, Any]
)
@limiter.limit("60/minute")
async def get_items(
    request: Request,
    skip: int = 0, 
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
):
    """Obtener lista de items (requiere autenticación)"""
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
    
    logger.info(f"User {current_user.username} fetching items: skip={skip}, limit={limit}, total={total}")
    
    return {
        "success": True,
        "count": total,
        "skip": skip,
        "limit": limit,
        "data": items[skip:skip+limit]
    }


# GET single item (protegido)
@app.get(
    "/items/{item_id}",
    summary="Obtener Item",
    description="Obtener un item específico por su ID",
    tags=["Items"],
    response_model=Dict[str, Any]
)
async def get_item(
    item_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Obtener item por ID"""
    if item_id not in db:
        logger.warning(f"Item not found: {item_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} no encontrado"
        )
    return {"success": True, "data": db[item_id]}


# POST create item (protegido)
@app.post(
    "/items",
    status_code=status.HTTP_201_CREATED,
    summary="Crear Item",
    description="Crear un nuevo item en la base de datos",
    tags=["Items"],
    response_model=Dict[str, Any]
)
async def create_item(
    item: ItemCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Crear nuevo item"""
    item_id = str(uuid.uuid4())
    new_item = Item(
        id=item_id,
        **item.model_dump(),
        created_at=datetime.utcnow().isoformat()
    )
    db[item_id] = new_item
    
    logger.info(f"User {current_user.username} created item: {item_id}")
    
    return {"success": True, "data": new_item}


# PUT update item (protegido)
@app.put(
    "/items/{item_id}",
    summary="Actualizar Item",
    description="Actualizar un item existente",
    tags=["Items"],
    response_model=Dict[str, Any]
)
async def update_item(
    item_id: str, 
    item_update: ItemUpdate,
    current_user: User = Depends(get_current_active_user)
):
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
    
    logger.info(f"User {current_user.username} updated item: {item_id}")
    
    return {"success": True, "data": existing}


# DELETE item (protegido)
@app.delete(
    "/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar Item",
    description="Eliminar un item por su ID",
    tags=["Items"]
)
async def delete_item(
    item_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Eliminar item"""
    if item_id not in db:
        logger.warning(f"Item not found for delete: {item_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} no encontrado"
        )
    
    del db[item_id]
    
    logger.info(f"User {current_user.username} deleted item: {item_id}")
    
    return None


# Stats endpoint (protegido)
@app.get(
    "/stats",
    summary="Estadísticas",
    description="Obtener estadísticas de uso de la API",
    tags=["Stats"],
    response_model=Dict[str, Any]
)
async def get_stats(current_user: User = Depends(get_current_active_user)):
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
