"""
Modelos Pydantic para validación
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ItemBase(BaseModel):
    """Base item model"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = None

class ItemCreate(ItemBase):
    """Schema para crear items"""
    pass

class ItemUpdate(BaseModel):
    """Schema para actualizar items"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = None

class Item(ItemBase):
    """Schema completo de item"""
    id: str
    created_at: str
    updated_at: Optional[str] = None
    
    class Config:
        from_attributes = True
