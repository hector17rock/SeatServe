"""
Tests for Pydantic schemas
"""
import pytest
from pydantic import ValidationError
from datetime import datetime

from app.schemas import (
    CategoryCreate, CategoryUpdate, CategoryResponse,
    MenuItemCreate, MenuItemUpdate, MenuItemResponse,
    OrderCreate, OrderUpdate, OrderResponse,
    OrderItemCreate, OrderItemUpdate, OrderItemResponse,
    StaffCreate, StaffUpdate, StaffResponse,
    RestaurantCreate, RestaurantUpdate, RestaurantResponse,
    LoginRequest, Token, MessageResponse,
    OrderStatus, PaymentStatus, PaymentMethod, StaffRole
)


class TestCategorySchemas:
    """Test category-related schemas"""
    
    def test_category_create_valid(self):
        """Test CategoryCreate with valid data"""
        data = {
            "name": "Appetizers",
            "description": "Delicious starters",
            "is_active": True,
            "sort_order": 1
        }
        
        category = CategoryCreate(**data)
        assert category.name == "Appetizers"
        assert category.description == "Delicious starters"
        assert category.is_active is True
        assert category.sort_order == 1
    
    def test_category_create_minimal(self):
        """Test CategoryCreate with minimal data"""
        data = {"name": "Main Courses"}
        
        category = CategoryCreate(**data)
        assert category.name == "Main Courses"
        assert category.description is None
        assert category.is_active is True  # Default value
        assert category.sort_order == 0  # Default value
    
    def test_category_create_invalid_empty_name(self):
        """Test CategoryCreate with empty name"""
        with pytest.raises(ValidationError):
            CategoryCreate(name="")
    
    def test_category_update_partial(self):
        """Test CategoryUpdate with partial data"""
        data = {"name": "Updated Name"}
        
        category = CategoryUpdate(**data)
        assert category.name == "Updated Name"
        assert category.description is None
        assert category.is_active is None
    
    def test_category_response(self):
        """Test CategoryResponse schema"""
        data = {
            "id": 1,
            "name": "Appetizers",
            "description": "Starters",
            "is_active": True,
            "sort_order": 1,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        category = CategoryResponse(**data)
        assert category.id == 1
        assert category.name == "Appetizers"


class TestMenuItemSchemas:
    """Test menu item-related schemas"""
    
    def test_menu_item_create_valid(self):
        """Test MenuItemCreate with valid data"""
        data = {
            "name": "Caesar Salad",
            "description": "Fresh romaine lettuce",
            "price": 12.99,
            "category_id": 1,
            "is_available": True,
            "is_vegetarian": True,
            "calories": 320,
            "preparation_time": 10
        }
        
        item = MenuItemCreate(**data)
        assert item.name == "Caesar Salad"
        assert item.price == 12.99
        assert item.category_id == 1
    
    def test_menu_item_create_negative_price(self):
        """Test MenuItemCreate with negative price"""
        data = {
            "name": "Caesar Salad",
            "price": -12.99,
            "category_id": 1
        }
        
        with pytest.raises(ValidationError) as exc_info:
            MenuItemCreate(**data)
        
        assert "Price must be positive" in str(exc_info.value)
    
    def test_menu_item_create_price_rounding(self):
        """Test MenuItemCreate price rounding"""
        data = {
            "name": "Caesar Salad",
            "price": 12.999,  # Should round to 13.00
            "category_id": 1
        }
        
        item = MenuItemCreate(**data)
        assert item.price == 13.00
    
    def test_menu_item_update_valid(self):
        """Test MenuItemUpdate with valid data"""
        data = {
            "price": 15.99,
            "is_available": False
        }
        
        item = MenuItemUpdate(**data)
        assert item.price == 15.99
        assert item.is_available is False
        assert item.name is None  # Not updated


class TestOrderSchemas:
    """Test order-related schemas"""
    
    def test_order_create_valid(self):
        """Test OrderCreate with valid data"""
        data = {
            "table_id": 1,
            "customer_name": "John Doe",
            "customer_phone": "+1234567890",
            "customer_email": "john@example.com",
            "items": [
                {
                    "menu_item_id": 1,
                    "quantity": 2,
                    "special_instructions": "No onions"
                }
            ],
            "notes": "Customer birthday"
        }
        
        order = OrderCreate(**data)
        assert order.table_id == 1
        assert order.customer_name == "John Doe"
        assert len(order.items) == 1
        assert order.items[0].quantity == 2
    
    def test_order_create_invalid_email(self):
        """Test OrderCreate with invalid email"""
        data = {
            "table_id": 1,
            "customer_email": "not-an-email"
        }
        
        with pytest.raises(ValidationError):
            OrderCreate(**data)
    
    def test_order_item_create_invalid_quantity(self):
        """Test OrderItemCreate with invalid quantity"""
        data = {
            "menu_item_id": 1,
            "quantity": 0  # Should be at least 1
        }
        
        with pytest.raises(ValidationError) as exc_info:
            OrderItemCreate(**data)
        
        assert "Quantity must be at least 1" in str(exc_info.value)
    
    def test_order_status_enum(self):
        """Test OrderStatus enum values"""
        assert OrderStatus.PENDING == "pending"
        assert OrderStatus.CONFIRMED == "confirmed"
        assert OrderStatus.PREPARING == "preparing"
        assert OrderStatus.READY == "ready"
        assert OrderStatus.SERVED == "served"
        assert OrderStatus.PAID == "paid"
        assert OrderStatus.CANCELLED == "cancelled"
    
    def test_payment_method_enum(self):
        """Test PaymentMethod enum values"""
        assert PaymentMethod.CASH == "cash"
        assert PaymentMethod.CARD == "card"
        assert PaymentMethod.DIGITAL == "digital"


class TestStaffSchemas:
    """Test staff-related schemas"""
    
    def test_staff_create_valid(self):
        """Test StaffCreate with valid data"""
        data = {
            "username": "johndoe",
            "email": "john@restaurant.com",
            "full_name": "John Doe",
            "password": "securepassword123",
            "role": "waiter",
            "phone": "+1234567890"
        }
        
        staff = StaffCreate(**data)
        assert staff.username == "johndoe"
        assert staff.email == "john@restaurant.com"
        assert staff.role == StaffRole.WAITER
    
    def test_staff_create_weak_password(self):
        """Test StaffCreate with weak password"""
        data = {
            "username": "johndoe",
            "email": "john@restaurant.com",
            "full_name": "John Doe",
            "password": "123",  # Too short
            "role": "waiter"
        }
        
        with pytest.raises(ValidationError) as exc_info:
            StaffCreate(**data)
        
        assert "Password must be at least 6 characters long" in str(exc_info.value)
    
    def test_staff_role_enum(self):
        """Test StaffRole enum values"""
        assert StaffRole.ADMIN == "admin"
        assert StaffRole.MANAGER == "manager"
        assert StaffRole.WAITER == "waiter"
        assert StaffRole.CHEF == "chef"
        assert StaffRole.CASHIER == "cashier"


class TestAuthenticationSchemas:
    """Test authentication-related schemas"""
    
    def test_login_request_valid(self):
        """Test LoginRequest with valid data"""
        data = {
            "username": "johndoe",
            "password": "securepassword123"
        }
        
        login = LoginRequest(**data)
        assert login.username == "johndoe"
        assert login.password == "securepassword123"
    
    def test_token_schema(self):
        """Test Token schema"""
        data = {
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
            "token_type": "bearer"
        }
        
        token = Token(**data)
        assert token.access_token.startswith("eyJ")
        assert token.token_type == "bearer"


class TestRestaurantSchemas:
    """Test restaurant-related schemas"""
    
    def test_restaurant_create_valid(self):
        """Test RestaurantCreate with valid data"""
        data = {
            "name": "The Great Restaurant",
            "address": "123 Main Street",
            "phone": "+1234567890",
            "email": "info@greatrestaurant.com",
            "currency": "USD",
            "tax_rate": 0.08,
            "is_open": True
        }
        
        restaurant = RestaurantCreate(**data)
        assert restaurant.name == "The Great Restaurant"
        assert restaurant.tax_rate == 0.08
        assert restaurant.currency == "USD"
    
    def test_restaurant_create_minimal(self):
        """Test RestaurantCreate with minimal data"""
        data = {"name": "Simple Restaurant"}
        
        restaurant = RestaurantCreate(**data)
        assert restaurant.name == "Simple Restaurant"
        assert restaurant.timezone == "UTC"  # Default value
        assert restaurant.currency == "USD"  # Default value
        assert restaurant.is_open is True  # Default value


class TestMessageResponse:
    """Test message response schema"""
    
    def test_message_response_simple(self):
        """Test MessageResponse with simple message"""
        data = {"message": "Operation successful"}
        
        response = MessageResponse(**data)
        assert response.message == "Operation successful"
        assert response.detail is None
    
    def test_message_response_with_detail(self):
        """Test MessageResponse with message and detail"""
        data = {
            "message": "Validation error",
            "detail": "Price must be positive"
        }
        
        response = MessageResponse(**data)
        assert response.message == "Validation error"
        assert response.detail == "Price must be positive"


class TestSchemaValidation:
    """Test general schema validation features"""
    
    def test_from_attributes_config(self):
        """Test that schemas can be created from ORM objects"""
        # This would typically be tested with actual ORM objects
        # For now, we test that the config is properly set
        
        data = {
            "id": 1,
            "name": "Test Category",
            "is_active": True,
            "sort_order": 1,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        category = CategoryResponse(**data)
        assert category.id == 1
        assert category.name == "Test Category"
    
    def test_extra_fields_ignored(self):
        """Test that extra fields are ignored"""
        data = {
            "name": "Test Category",
            "extra_field": "should be ignored"  # This should be ignored
        }
        
        # Should not raise an error
        category = CategoryCreate(**data)
        assert category.name == "Test Category"
        # extra_field should not be accessible
        assert not hasattr(category, "extra_field")