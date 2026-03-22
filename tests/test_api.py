"""
Test suite for FastAPI REST API
Tests security, endpoints, and validation
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoint"""
    
    def test_health_returns_200(self):
        """Health check should return 200"""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_status(self):
        """Should return healthy status"""
        response = client.get("/health")
        assert response.json()["status"] == "healthy"
    
    def test_health_includes_uptime(self):
        """Should include uptime"""
        response = client.get("/health")
        assert "uptime" in response.json()


class TestItemsCRUD:
    """Test items CRUD operations"""
    
    def test_create_item(self):
        """Should create new item"""
        item_data = {
            "name": "Test Product",
            "description": "Test description",
            "price": 99.99,
            "in_stock": True
        }
        response = client.post("/items", json=item_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == item_data["name"]
        assert "id" in data
    
    def test_get_all_items(self):
        """Should return list of items"""
        response = client.get("/items")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_item_by_id(self):
        """Should return item by ID"""
        # First create
        create_response = client.post("/items", json={
            "name": "Get Test",
            "price": 10
        })
        item_id = create_response.json()["id"]
        
        # Then get
        response = client.get(f"/items/{item_id}")
        assert response.status_code == 200
        assert response.json()["id"] == item_id
    
    def test_update_item(self):
        """Should update existing item"""
        # Create
        create_response = client.post("/items", json={
            "name": "Original",
            "price": 10
        })
        item_id = create_response.json()["id"]
        
        # Update
        response = client.put(f"/items/{item_id}", json={
            "name": "Updated",
            "price": 20
        })
        assert response.status_code == 200
        assert response.json()["name"] == "Updated"
    
    def test_delete_item(self):
        """Should delete item"""
        # Create
        create_response = client.post("/items", json={
            "name": "Delete Me",
            "price": 5
        })
        item_id = create_response.json()["id"]
        
        # Delete
        response = client.delete(f"/items/{item_id}")
        assert response.status_code == 200
        
        # Verify deleted
        get_response = client.get(f"/items/{item_id}")
        assert get_response.status_code == 404
    
    def test_get_nonexistent_item(self):
        """Should return 404 for non-existent item"""
        response = client.get("/items/99999")
        assert response.status_code == 404


class TestValidation:
    """Test input validation"""
    
    def test_missing_required_field(self):
        """Should reject item without name"""
        response = client.post("/items", json={"price": 10})
        assert response.status_code == 422
    
    def test_invalid_price_type(self):
        """Should reject non-numeric price"""
        response = client.post("/items", json={
            "name": "Test",
            "price": "not-a-number"
        })
        assert response.status_code == 422
    
    def test_negative_price(self):
        """Should reject negative price"""
        response = client.post("/items", json={
            "name": "Test",
            "price": -10
        })
        assert response.status_code == 422
    
    def test_name_too_long(self):
        """Should reject too long name"""
        response = client.post("/items", json={
            "name": "a" * 200,
            "price": 10
        })
        assert response.status_code == 422


class TestPagination:
    """Test pagination"""
    
    def test_pagination_parameters(self):
        """Should accept skip and limit"""
        response = client.get("/items?skip=0&limit=10")
        assert response.status_code == 200
    
    def test_negative_skip(self):
        """Should reject negative skip"""
        response = client.get("/items?skip=-1")
        assert response.status_code == 422
    
    def test_limit_too_high(self):
        """Should reject too high limit"""
        response = client.get("/items?limit=1000")
        assert response.status_code == 422


class TestStats:
    """Test statistics endpoint"""
    
    def test_stats_endpoint(self):
        """Should return statistics"""
        response = client.get("/stats")
        assert response.status_code == 200
        data = response.json()
        assert "total_items" in data
        assert "total_value" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
