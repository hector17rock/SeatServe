"""
Tests for orders router endpoints
"""
import pytest
from fastapi.testclient import TestClient


class TestOrderEndpoints:
    """Test order management endpoints"""
    
    def test_get_orders_empty(self, client):
        """Test getting orders when none exist"""
        response = client.get("/api/v1/orders/")
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_create_order_success(self, client, sample_table, sample_menu_item, order_data):
        """Test creating a new order successfully"""
        order_data["table_id"] = sample_table.id
        order_data["items"][0]["menu_item_id"] = sample_menu_item.id
        
        response = client.post("/api/v1/orders/", json=order_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["table_id"] == sample_table.id
        assert data["customer_name"] == order_data["customer_name"]
        assert data["status"] == "pending"
        assert len(data["order_items"]) == 1
        assert "id" in data
        assert data["total"] > 0
    
    def test_create_order_invalid_table(self, client, sample_menu_item, order_data):
        """Test creating order with invalid table"""
        order_data["table_id"] = 999  # Non-existent table
        order_data["items"][0]["menu_item_id"] = sample_menu_item.id
        
        response = client.post("/api/v1/orders/", json=order_data)
        
        assert response.status_code == 400
        assert "not found" in response.json()["message"]
    
    def test_create_order_unavailable_table(self, client, sample_table, sample_menu_item, order_data, db_session):
        """Test creating order with unavailable table"""
        # Make table unavailable
        sample_table.is_available = False
        db_session.commit()
        
        order_data["table_id"] = sample_table.id
        order_data["items"][0]["menu_item_id"] = sample_menu_item.id
        
        response = client.post("/api/v1/orders/", json=order_data)
        
        assert response.status_code == 400
        assert "not available" in response.json()["message"]
    
    def test_create_order_invalid_menu_item(self, client, sample_table, order_data):
        """Test creating order with invalid menu item"""
        order_data["table_id"] = sample_table.id
        order_data["items"][0]["menu_item_id"] = 999  # Non-existent menu item
        
        response = client.post("/api/v1/orders/", json=order_data)
        
        assert response.status_code == 400
        assert "not found" in response.json()["message"]
    
    def test_create_order_unavailable_menu_item(self, client, sample_table, sample_menu_item, order_data, db_session):
        """Test creating order with unavailable menu item"""
        # Make menu item unavailable
        sample_menu_item.is_available = False
        db_session.commit()
        
        order_data["table_id"] = sample_table.id
        order_data["items"][0]["menu_item_id"] = sample_menu_item.id
        
        response = client.post("/api/v1/orders/", json=order_data)
        
        assert response.status_code == 400
        assert "not available" in response.json()["message"]
    
    def test_get_orders_with_data(self, client, sample_order):
        """Test getting orders when they exist"""
        response = client.get("/api/v1/orders/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == sample_order.id
    
    def test_get_order_by_id_success(self, client, sample_order):
        """Test getting a specific order by ID"""
        response = client.get(f"/api/v1/orders/{sample_order.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_order.id
        assert data["customer_name"] == sample_order.customer_name
    
    def test_get_order_by_id_not_found(self, client):
        """Test getting order with non-existent ID"""
        response = client.get("/api/v1/orders/999")
        
        assert response.status_code == 404
    
    def test_update_order_success(self, client, sample_order):
        """Test updating an order successfully"""
        update_data = {
            "customer_name": "Updated Customer",
            "status": "confirmed",
            "notes": "Updated notes"
        }
        
        response = client.put(f"/api/v1/orders/{sample_order.id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["customer_name"] == "Updated Customer"
        assert data["status"] == "confirmed"
        assert data["notes"] == "Updated notes"
    
    def test_update_order_not_found(self, client):
        """Test updating non-existent order"""
        update_data = {"customer_name": "Updated Customer"}
        
        response = client.put("/api/v1/orders/999", json=update_data)
        
        assert response.status_code == 404
    
    def test_cancel_order_success(self, client, sample_order):
        """Test cancelling an order successfully"""
        response = client.delete(f"/api/v1/orders/{sample_order.id}")
        
        assert response.status_code == 200
        assert "cancelled successfully" in response.json()["message"]
    
    def test_cancel_completed_order(self, client, sample_order, db_session):
        """Test cancelling a completed order"""
        # Set order as paid
        sample_order.status = "paid"
        db_session.commit()
        
        response = client.delete(f"/api/v1/orders/{sample_order.id}")
        
        assert response.status_code == 400
        assert "Cannot cancel" in response.json()["message"]


class TestOrderItemEndpoints:
    """Test order item management endpoints"""
    
    def test_add_item_to_order_success(self, client, sample_order, sample_category, db_session):
        """Test adding an item to an existing order"""
        # Create a new menu item for adding
        from app.models import MenuItem
        new_item = MenuItem(
            name="New Item",
            price=8.99,
            category_id=sample_category.id,
            is_available=True
        )
        db_session.add(new_item)
        db_session.commit()
        
        item_data = {
            "menu_item_id": new_item.id,
            "quantity": 2,
            "special_instructions": "Extra sauce"
        }
        
        response = client.post(f"/api/v1/orders/{sample_order.id}/items", json=item_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["menu_item_id"] == new_item.id
        assert data["quantity"] == 2
        assert data["special_instructions"] == "Extra sauce"
        assert data["total_price"] == 8.99 * 2
    
    def test_add_item_to_completed_order(self, client, sample_order, sample_menu_item, db_session):
        """Test adding item to completed order"""
        # Set order as paid
        sample_order.status = "paid"
        db_session.commit()
        
        item_data = {
            "menu_item_id": sample_menu_item.id,
            "quantity": 1
        }
        
        response = client.post(f"/api/v1/orders/{sample_order.id}/items", json=item_data)
        
        assert response.status_code == 400
        assert "Cannot modify" in response.json()["message"]
    
    def test_remove_item_from_order_success(self, client, sample_order_item):
        """Test removing an item from an order"""
        response = client.delete(f"/api/v1/orders/{sample_order_item.order_id}/items/{sample_order_item.id}")
        
        assert response.status_code == 200
        assert "removed" in response.json()["message"]
    
    def test_remove_item_from_completed_order(self, client, sample_order, sample_order_item, db_session):
        """Test removing item from completed order"""
        # Set order as paid
        sample_order.status = "paid"
        db_session.commit()
        
        response = client.delete(f"/api/v1/orders/{sample_order_item.order_id}/items/{sample_order_item.id}")
        
        assert response.status_code == 400
        assert "Cannot modify" in response.json()["message"]


class TestOrderStatusManagement:
    """Test order status management endpoints"""
    
    def test_update_order_status_success(self, client, sample_order):
        """Test updating order status successfully"""
        response = client.patch(f"/api/v1/orders/{sample_order.id}/status?new_status=confirmed")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "confirmed"
    
    def test_update_order_status_invalid_transition(self, client, sample_order):
        """Test invalid status transition"""
        # Try to go from pending directly to served (should go through confirmed, preparing, ready first)
        response = client.patch(f"/api/v1/orders/{sample_order.id}/status?new_status=served")
        
        assert response.status_code == 400
        assert "Invalid status transition" in response.json()["message"]
    
    def test_order_status_workflow(self, client, sample_order):
        """Test complete order status workflow"""
        # pending -> confirmed
        response = client.patch(f"/api/v1/orders/{sample_order.id}/status?new_status=confirmed")
        assert response.status_code == 200
        assert response.json()["status"] == "confirmed"
        
        # confirmed -> preparing
        response = client.patch(f"/api/v1/orders/{sample_order.id}/status?new_status=preparing")
        assert response.status_code == 200
        assert response.json()["status"] == "preparing"
        
        # preparing -> ready
        response = client.patch(f"/api/v1/orders/{sample_order.id}/status?new_status=ready")
        assert response.status_code == 200
        assert response.json()["status"] == "ready"
        
        # ready -> served
        response = client.patch(f"/api/v1/orders/{sample_order.id}/status?new_status=served")
        assert response.status_code == 200
        assert response.json()["status"] == "served"
        
        # served -> paid
        response = client.patch(f"/api/v1/orders/{sample_order.id}/status?new_status=paid")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "paid"
        assert data["completed_at"] is not None


class TestOrderTableIntegration:
    """Test order and table integration"""
    
    def test_get_active_order_by_table(self, client, sample_order, sample_table):
        """Test getting active order for a table"""
        response = client.get(f"/api/v1/orders/table/{sample_table.id}/active")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_order.id
        assert data["table_id"] == sample_table.id
    
    def test_get_active_order_no_active_order(self, client, sample_table):
        """Test getting active order when table has no active order"""
        response = client.get(f"/api/v1/orders/table/{sample_table.id}/active")
        
        assert response.status_code == 200
        assert response.json() is None
    
    def test_get_active_order_invalid_table(self, client):
        """Test getting active order for non-existent table"""
        response = client.get("/api/v1/orders/table/999/active")
        
        assert response.status_code == 404
    
    def test_table_availability_after_order_completion(self, client, sample_order, sample_table, db_session):
        """Test that table becomes available after order completion"""
        # Set table as unavailable since it has an active order
        sample_table.is_available = False
        db_session.commit()
        db_session.refresh(sample_table)
        assert sample_table.is_available is False
        
        # Complete the order
        response = client.patch(f"/api/v1/orders/{sample_order.id}/status?new_status=confirmed")
        assert response.status_code == 200
        
        response = client.patch(f"/api/v1/orders/{sample_order.id}/status?new_status=preparing")
        assert response.status_code == 200
        
        response = client.patch(f"/api/v1/orders/{sample_order.id}/status?new_status=ready")
        assert response.status_code == 200
        
        response = client.patch(f"/api/v1/orders/{sample_order.id}/status?new_status=served")
        assert response.status_code == 200
        
        response = client.patch(f"/api/v1/orders/{sample_order.id}/status?new_status=paid")
        assert response.status_code == 200
        
        # Now table should be available
        db_session.refresh(sample_table)
        assert sample_table.is_available is True


class TestOrderFiltering:
    """Test order filtering and querying"""
    
    def test_filter_orders_by_status(self, client, db_session, sample_table):
        """Test filtering orders by status"""
        from app.models import Order
        
        # Create orders with different statuses
        pending_order = Order(
            table_id=sample_table.id,
            customer_name="Pending Customer",
            status="pending"
        )
        confirmed_order = Order(
            table_id=sample_table.id,
            customer_name="Confirmed Customer", 
            status="confirmed"
        )
        
        db_session.add(pending_order)
        db_session.add(confirmed_order)
        db_session.commit()
        
        # Filter by pending status
        response = client.get("/api/v1/orders/?status=pending")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["status"] == "pending"
        
        # Filter by confirmed status
        response = client.get("/api/v1/orders/?status=confirmed")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["status"] == "confirmed"
    
    def test_filter_orders_by_table(self, client, db_session, sample_table):
        """Test filtering orders by table"""
        from app.models import Order, Table
        
        # Create another table and order
        table2 = Table(number=2, capacity=2, is_available=True)
        db_session.add(table2)
        db_session.flush()
        
        order1 = Order(table_id=sample_table.id, customer_name="Customer 1")
        order2 = Order(table_id=table2.id, customer_name="Customer 2")
        
        db_session.add(order1)
        db_session.add(order2)
        db_session.commit()
        
        # Filter by table 1
        response = client.get(f"/api/v1/orders/?table_id={sample_table.id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["table_id"] == sample_table.id
    
    def test_orders_pagination(self, client, db_session, sample_table):
        """Test order pagination"""
        from app.models import Order
        
        # Create multiple orders
        orders = []
        for i in range(5):
            order = Order(
                table_id=sample_table.id,
                customer_name=f"Customer {i}",
                status="pending"
            )
            orders.append(order)
            db_session.add(order)
        db_session.commit()
        
        # Test with limit
        response = client.get("/api/v1/orders/?limit=3")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        
        # Test with skip and limit
        response = client.get("/api/v1/orders/?skip=2&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2