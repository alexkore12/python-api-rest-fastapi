"""
Base de datos en memoria (simulada)
"""
from typing import Dict
from models import Item

# In-memory storage
items_db: Dict[str, Item] = {}

# Seed data
items_db["1"] = Item(
    id="1",
    name="Producto de ejemplo",
    description="Descripción del producto",
    price=99.99,
    category="electronics",
    created_at="2024-01-01T00:00:00",
    updated_at="2024-01-01T00:00:00"
)
