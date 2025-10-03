"""
Tests for menu router endpoints
"""
import pytest
from fastapi.testclient import TestClient


class TestCategoryEndpoints:
    """Test category management endpoints"""
    
    def test_get_categories_empty(self, client):
        """Test getting categories when none exist"""
        response = client.get("/api/v1/menu/categories")
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_create_category_success(self, client, category_data):
        """Test creating a new category successfully"""
        response = client.post("/api/v1/menu/categories", json=category_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == category_data["name"]
        assert data["description"] == category_data["description"]
        assert "id" in data
        assert "created_at" in data
    
    def test_create_category_duplicate_name(self, client, sample_category, category_data):
        """Test creating category with duplicate name"""
        category_data["name"] = sample_category.name
        
        response = client.post("/api/v1/menu/categories", json=category_data)
        
        assert response.status_code == 400
        assert "already exists" in response.json()["message"]
    
    def test_get_categories_with_data(self, client, sample_category):
        """Test getting categories when they exist"""
        response = client.get("/api/v1/menu/categories")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == sample_category.name
    
    def test_get_category_by_id_success(self, client, sample_category):
        """Test getting a specific category by ID"""
        response = client.get(f"/api/v1/menu/categories/{sample_category.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_category.id
        assert data["name"] == sample_category.name
    
    def test_get_category_by_id_not_found(self, client):
        """Test getting category with non-existent ID"""
        response = client.get("/api/v1/menu/categories/999")
        
        assert response.status_code == 404
        assert "not found" in response.json()["message"]
    
    def test_update_category_success(self, client, sample_category):
        """Test updating a category successfully"""
        update_data = {
            "name": "Updated Category",
            "description": "Updated description"
        }
        
        response = client.put(f"/api/v1/menu/categories/{sample_category.id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Category"
        assert data["description"] == "Updated description"
    
    def test_update_category_not_found(self, client):
        """Test updating non-existent category"""
        update_data = {"name": "Updated Category"}
        
        response = client.put("/api/v1/menu/categories/999", json=update_data)
        
        assert response.status_code == 404
    
    def test_delete_category_success(self, client, sample_category):
        """Test deleting a category successfully"""
        response = client.delete(f"/api/v1/menu/categories/{sample_category.id}")
        
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"]
    
    def test_delete_category_with_items(self, client, sample_menu_item, sample_category):
        """Test deleting category that has menu items"""
        response = client.delete(f"/api/v1/menu/categories/{sample_category.id}")
        
        assert response.status_code == 400
        assert "menu items" in response.json()["message"]


class TestMenuItemEndpoints:
    """Test menu item management endpoints"""
    
    def test_get_menu_items_empty(self, client):
        """Test getting menu items when none exist"""
        response = client.get("/api/v1/menu/items")
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_create_menu_item_success(self, client, sample_category, menu_item_data):
        """Test creating a new menu item successfully"""
        menu_item_data["category_id"] = sample_category.id
        
        response = client.post("/api/v1/menu/items", json=menu_item_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == menu_item_data["name"]
        assert data["price"] == menu_item_data["price"]
        assert data["category_id"] == sample_category.id
        assert "id" in data
    
    def test_create_menu_item_invalid_category(self, client, menu_item_data):
        """Test creating menu item with invalid category"""
        menu_item_data["category_id"] = 999  # Non-existent category
        
        response = client.post("/api/v1/menu/items", json=menu_item_data)
        
        assert response.status_code == 400
        assert "not found" in response.json()["message"]
    
    def test_create_menu_item_duplicate_name(self, client, sample_menu_item, menu_item_data):
        """Test creating menu item with duplicate name in same category"""
        menu_item_data["name"] = sample_menu_item.name
        menu_item_data["category_id"] = sample_menu_item.category_id
        
        response = client.post("/api/v1/menu/items", json=menu_item_data)
        
        assert response.status_code == 400
        assert "already exists" in response.json()["message"]
    
    def test_get_menu_items_with_data(self, client, sample_menu_item):
        """Test getting menu items when they exist"""
        response = client.get("/api/v1/menu/items")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == sample_menu_item.name
    
    def test_get_menu_items_by_category(self, client, sample_menu_item):
        """Test filtering menu items by category"""
        response = client.get(f"/api/v1/menu/items?category_id={sample_menu_item.category_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["category_id"] == sample_menu_item.category_id
    
    def test_get_menu_items_search(self, client, sample_menu_item):
        """Test searching menu items"""
        search_term = sample_menu_item.name[:5]  # First 5 characters
        response = client.get(f"/api/v1/menu/items?search={search_term}")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert sample_menu_item.name.lower().startswith(search_term.lower())
    
    def test_get_menu_item_by_id_success(self, client, sample_menu_item):
        """Test getting a specific menu item by ID"""
        response = client.get(f"/api/v1/menu/items/{sample_menu_item.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_menu_item.id
        assert data["name"] == sample_menu_item.name
    
    def test_get_menu_item_by_id_not_found(self, client):
        """Test getting menu item with non-existent ID"""
        response = client.get("/api/v1/menu/items/999")
        
        assert response.status_code == 404
    
    def test_update_menu_item_success(self, client, sample_menu_item):
        """Test updating a menu item successfully"""
        update_data = {
            "name": "Updated Item",
            "price": 19.99,
            "is_available": False
        }
        
        response = client.put(f"/api/v1/menu/items/{sample_menu_item.id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Item"
        assert data["price"] == 19.99
        assert data["is_available"] is False
    
    def test_toggle_item_availability(self, client, sample_menu_item):
        """Test toggling menu item availability"""
        response = client.patch(f"/api/v1/menu/items/{sample_menu_item.id}/availability?available=false")
        
        assert response.status_code == 200
        data = response.json()
        assert data["is_available"] is False
    
    def test_delete_menu_item_success(self, client, sample_menu_item):
        """Test deleting a menu item successfully"""
        response = client.delete(f"/api/v1/menu/items/{sample_menu_item.id}")
        
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"]
    
    def test_get_category_items(self, client, sample_menu_item, sample_category):
        """Test getting items for a specific category"""
        response = client.get(f"/api/v1/menu/categories/{sample_category.id}/items")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["category_id"] == sample_category.id
    
    def test_get_category_items_not_found(self, client):
        """Test getting items for non-existent category"""
        response = client.get("/api/v1/menu/categories/999/items")
        
        assert response.status_code == 404


class TestMenuPagination:
    """Test pagination in menu endpoints"""
    
    def test_categories_pagination(self, client, db_session):
        """Test pagination for categories"""
        # Create multiple categories
        from app.models import Category
        categories = []
        for i in range(5):
            category = Category(
                name=f"Category {i}",
                description=f"Description {i}",
                sort_order=i
            )
            categories.append(category)
            db_session.add(category)
        db_session.commit()
        
        # Test with limit
        response = client.get("/api/v1/menu/categories?limit=3")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        
        # Test with skip and limit
        response = client.get("/api/v1/menu/categories?skip=2&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
    
    def test_menu_items_pagination(self, client, db_session, sample_category):
        """Test pagination for menu items"""
        # Create multiple menu items
        from app.models import MenuItem
        items = []
        for i in range(5):
            item = MenuItem(
                name=f"Item {i}",
                description=f"Description {i}",
                price=10.0 + i,
                category_id=sample_category.id,
                sort_order=i
            )
            items.append(item)
            db_session.add(item)
        db_session.commit()
        
        # Test with limit
        response = client.get("/api/v1/menu/items?limit=3")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3


class TestMenuFiltering:
    """Test filtering functionality in menu endpoints"""
    
    def test_active_categories_only(self, client, db_session):
        """Test filtering categories by active status"""
        from app.models import Category
        
        # Create active and inactive categories
        active_cat = Category(name="Active Category", is_active=True)
        inactive_cat = Category(name="Inactive Category", is_active=False)
        
        db_session.add(active_cat)
        db_session.add(inactive_cat)
        db_session.commit()
        
        # Test active only (default)
        response = client.get("/api/v1/menu/categories?active_only=true")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Active Category"
        
        # Test include inactive
        response = client.get("/api/v1/menu/categories?active_only=false")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
    
    def test_available_items_only(self, client, db_session, sample_category):
        """Test filtering menu items by availability"""
        from app.models import MenuItem
        
        # Create available and unavailable items
        available_item = MenuItem(
            name="Available Item",
            price=10.0,
            category_id=sample_category.id,
            is_available=True
        )
        unavailable_item = MenuItem(
            name="Unavailable Item",
            price=15.0,
            category_id=sample_category.id,
            is_available=False
        )
        
        db_session.add(available_item)
        db_session.add(unavailable_item)
        db_session.commit()
        
        # Test available only (default)
        response = client.get("/api/v1/menu/items?available_only=true")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Available Item"
        
        # Test include unavailable
        response = client.get("/api/v1/menu/items?available_only=false")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2