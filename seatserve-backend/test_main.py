#!/usr/bin/env python3
"""
Test suite for SeatServe FastAPI Backend
Tests all major endpoints and functionality
"""

import pytest
from fastapi.testclient import TestClient
from main import app, init_db, MenuItem, Order, Table
import json

# Initialize test client
client = TestClient(app)

# Setup - initialize database before tests
@pytest.fixture(scope="session", autouse=True)
def setup_db():
    """Initialize database for testing"""
    init_db()

class TestHealthEndpoint:
    """Test health check endpoint"""
    
    def test_health_check(self):
        """Test /health endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "SeatServe API"
        assert data["version"] == "1.0.0"
        print("[PASS] Health check endpoint")

class TestMenuEndpoints:
    """Test menu-related endpoints"""
    
    def test_get_menu(self):
        """Test GET /api/menu"""
        response = client.get("/api/menu")
        assert response.status_code == 200
        items = response.json()
        assert isinstance(items, list)
        assert len(items) > 0
        assert all(isinstance(item, dict) for item in items)
        print(f"[PASS] Get menu - {len(items)} items loaded")
    
    def test_get_menu_categories(self):
        """Test GET /api/menu/categories"""
        response = client.get("/api/menu/categories")
        assert response.status_code == 200
        data = response.json()
        assert "categories" in data
        assert isinstance(data["categories"], list)
        print(f"[PASS] Get categories - {len(data['categories'])} categories found")
    
    def test_create_menu_item(self):
        """Test POST /api/menu"""
        new_item = {
            "name": "Test Burger",
            "description": "A test burger",
            "price": 9.99,
            "category": "Mains",
            "available": True
        }
        response = client.post("/api/menu", json=new_item)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == new_item["name"]
        assert data["price"] == new_item["price"]
        assert "id" in data
        print(f"[PASS] Create menu item - ID: {data['id']}")

class TestOrderEndpoints:
    """Test order-related endpoints"""
    
    def test_get_orders(self):
        """Test GET /api/orders"""
        response = client.get("/api/orders")
        assert response.status_code == 200
        orders = response.json()
        assert isinstance(orders, list)
        print(f"[PASS] Get orders - {len(orders)} orders in system")
    
    def test_create_order(self):
        """Test POST /api/orders"""
        new_order = {
            "table_number": 1,
            "items": [
                {"id": "p1", "name": "Burger", "qty": 2, "price": 10.0}
            ],
            "total": 20.0,
            "status": "pending"
        }
        response = client.post("/api/orders", json=new_order)
        assert response.status_code == 200
        data = response.json()
        assert data["table_number"] == new_order["table_number"]
        assert data["total"] == new_order["total"]
        assert "id" in data
        assert "timestamp" in data
        print(f"[PASS] Create order - ID: {data['id']}, Total: ${data['total']}")

class TestTableEndpoints:
    """Test table-related endpoints"""
    
    def test_get_tables(self):
        """Test GET /api/tables"""
        response = client.get("/api/tables")
        assert response.status_code == 200
        tables = response.json()
        assert isinstance(tables, list)
        assert len(tables) > 0
        assert all(isinstance(table, dict) for table in tables)
        print(f"[PASS] Get tables - {len(tables)} tables available")
    
    def test_table_structure(self):
        """Test table data structure"""
        response = client.get("/api/tables")
        tables = response.json()
        first_table = tables[0]
        assert "id" in first_table
        assert "number" in first_table
        assert "seats" in first_table
        assert "status" in first_table
        print(f"[PASS] Table structure - Table {first_table['number']} has {first_table['seats']} seats")
    
    def test_update_table_status(self):
        """Test PUT /api/tables/{id}/status"""
        # Get first table
        response = client.get("/api/tables")
        tables = response.json()
        table_id = tables[0]["id"]
        
        # Update status
        response = client.put(f"/api/tables/{table_id}/status?status=occupied")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        print(f"[PASS] Update table status - Table {table_id} updated")
    
    def test_invalid_table_status(self):
        """Test invalid table status"""
        response = client.get("/api/tables")
        tables = response.json()
        table_id = tables[0]["id"]
        
        response = client.put(f"/api/tables/{table_id}/status?status=invalid_status")
        assert response.status_code == 400
        print("[PASS] Invalid status rejection")

class TestRootEndpoint:
    """Test root endpoint"""
    
    def test_root_endpoint(self):
        """Test GET /"""
        response = client.get("/")
        assert response.status_code == 200
        assert "SeatServe" in response.text
        assert "API" in response.text
        print("[PASS] Root endpoint")

class TestDataIntegrity:
    """Test data integrity and relationships"""
    
    def test_menu_item_price_valid(self):
        """Test that menu items have valid prices"""
        response = client.get("/api/menu")
        items = response.json()
        for item in items:
            assert item["price"] > 0
            assert isinstance(item["price"], (int, float))
        print(f"[PASS] Menu item prices valid - All {len(items)} items have positive prices")
    
    def test_order_total_calculation(self):
        """Test order total is positive"""
        response = client.get("/api/orders")
        orders = response.json()
        for order in orders:
            assert order["total"] >= 0
            assert isinstance(order["total"], (int, float))
        print(f"[PASS] Order totals valid - All {len(orders)} orders have valid totals")

class TestAPIDocumentation:
    """Test API documentation endpoints"""
    
    def test_docs_endpoint(self):
        """Test /docs endpoint exists"""
        response = client.get("/docs")
        assert response.status_code == 200
        print("[PASS] Swagger documentation available")

def run_all_tests():
    """Run all tests and return summary"""
    print("\n" + "="*50)
    print("SEATSERVE BACKEND TEST SUITE")
    print("="*50 + "\n")
    
    # Run pytest
    exit_code = pytest.main([__file__, "-v", "--tb=short"])
    
    return exit_code

if __name__ == "__main__":
    exit_code = run_all_tests()
    exit(exit_code)
