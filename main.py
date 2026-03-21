"""
FastAPI REST API - Aplicación principal
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime
import uuid

from models import Item, ItemCreate, ItemUpdate
from database import items_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager"""
    print("🚀 Starting API...")
    yield
    print("🛑 Shutting down API...")

app = FastAPI(
    title="FastAPI REST API",
    description="RESTful API con FastAPI y Pydantic",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory database
db = items_db

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime": "N/A"
    }

# GET all items
@app.get("/items", status_code=status.HTTP_200_OK)
async def get_items(skip: int = 0, limit: int = 100):
    """Obtener lista de items"""
    items = list(db.values())
    return {
        "success": True,
        "count": len(items),
        "data": items[skip:skip+limit]
    }

# GET single item
@app.get("/items/{item_id}")
async def get_item(item_id: str):
    """Obtener item por ID"""
    if item_id not in db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} no encontrado"
        )
    return {"success": True, "data": db[item_id]}

# POST create item
@app.post("/items", status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate):
    """Crear nuevo item"""
    item_id = str(uuid.uuid4())
    new_item = Item(
        id=item_id,
        **item.model_dump(),
        created_at=datetime.utcnow().isoformat()
    )
    db[item_id] = new_item
    return {"success": True, "data": new_item}

# PUT update item
@app.put("/items/{item_id}")
async def update_item(item_id: str, item_update: ItemUpdate):
    """Actualizar item existente"""
    if item_id not in db:
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
    
    return {"success": True, "data": existing}

# DELETE item
@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: str):
    """Eliminar item"""
    if item_id not in db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} no encontrado"
        )
    
    del db[item_id]
    return None

# Stats endpoint
@app.get("/stats")
async def get_stats():
    """Estadísticas de la API"""
    return {
        "total_items": len(db),
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
