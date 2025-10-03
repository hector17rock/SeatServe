"""
Test configuration and fixtures for SeatServe backend tests
"""
import pytest
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import tempfile
import os

from app.main import app
from app.db import get_db, Base
from app.models import Category, MenuItem, Table, Order, OrderItem, Staff, Restaurant
from app.utils import hash_password


# Test database URL - using SQLite for simplicity
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Set up test database"""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    yield
    # Clean up
    Base.metadata.drop_all(bind=engine)
    # Remove test database file
    try:
        os.unlink("test.db")
    except FileNotFoundError:
        pass


@pytest.fixture
def db_session():
    """Create a fresh database session for each test"""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # Clean up tables after each test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    """Create test client with database override"""
    app.dependency_overrides[get_db] = lambda: db_session
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up
    app.dependency_overrides.clear()


@pytest.fixture
def sample_category(db_session):
    """Create a sample category for testing"""
    category = Category(
        name="Appetizers",
        description="Delicious starters",
        is_active=True,
        sort_order=1
    )
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category


@pytest.fixture
def sample_menu_item(db_session, sample_category):
    """Create a sample menu item for testing"""
    menu_item = MenuItem(
        name="Caesar Salad",
        description="Fresh romaine lettuce with parmesan",
        price=12.99,
        category_id=sample_category.id,
        is_available=True,
        is_vegetarian=True,
        calories=320,
        preparation_time=10
    )
    db_session.add(menu_item)
    db_session.commit()
    db_session.refresh(menu_item)
    return menu_item


@pytest.fixture
def sample_table(db_session):
    """Create a sample table for testing"""
    table = Table(
        number=1,
        capacity=4,
        is_available=True,
        location="Window"
    )
    db_session.add(table)
    db_session.commit()
    db_session.refresh(table)
    return table


@pytest.fixture
def sample_order(db_session, sample_table):
    """Create a sample order for testing"""
    order = Order(
        table_id=sample_table.id,
        customer_name="John Doe",
        customer_phone="+1234567890",
        status="pending",
        subtotal=25.98,
        tax=2.08,
        total=28.06
    )
    db_session.add(order)
    db_session.commit()
    db_session.refresh(order)
    return order


@pytest.fixture
def sample_order_item(db_session, sample_order, sample_menu_item):
    """Create a sample order item for testing"""
    order_item = OrderItem(
        order_id=sample_order.id,
        menu_item_id=sample_menu_item.id,
        quantity=2,
        unit_price=12.99,
        total_price=25.98,
        special_instructions="No croutons"
    )
    db_session.add(order_item)
    db_session.commit()
    db_session.refresh(order_item)
    return order_item


@pytest.fixture
def sample_staff(db_session):
    """Create a sample staff member for testing"""
    staff = Staff(
        username="testuser",
        email="test@example.com",
        full_name="Test User",
        hashed_password=hash_password("testpassword123"),
        role="waiter",
        is_active=True,
        phone="+1234567890"
    )
    db_session.add(staff)
    db_session.commit()
    db_session.refresh(staff)
    return staff


@pytest.fixture
def sample_restaurant(db_session):
    """Create a sample restaurant configuration for testing"""
    restaurant = Restaurant(
        name="Test Restaurant",
        address="123 Test Street",
        phone="+1234567890",
        email="info@testrestaurant.com",
        currency="USD",
        tax_rate=0.08,
        is_open=True
    )
    db_session.add(restaurant)
    db_session.commit()
    db_session.refresh(restaurant)
    return restaurant


# Event loop fixture for async tests
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def auth_headers():
    """Mock authentication headers for protected endpoints"""
    return {"Authorization": "Bearer mock-jwt-token"}


# Test data fixtures
@pytest.fixture
def category_data():
    """Sample category data for POST requests"""
    return {
        "name": "Main Courses",
        "description": "Hearty main dishes",
        "is_active": True,
        "sort_order": 2
    }


@pytest.fixture
def menu_item_data():
    """Sample menu item data for POST requests"""
    return {
        "name": "Grilled Salmon",
        "description": "Fresh Atlantic salmon with herbs",
        "price": 24.99,
        "category_id": 1,
        "is_available": True,
        "is_vegetarian": False,
        "calories": 450,
        "preparation_time": 20
    }


@pytest.fixture
def order_data():
    """Sample order data for POST requests"""
    return {
        "table_id": 1,
        "customer_name": "Jane Smith",
        "customer_phone": "+1987654321",
        "customer_email": "jane@example.com",
        "items": [
            {
                "menu_item_id": 1,
                "quantity": 1,
                "special_instructions": "Medium rare"
            }
        ],
        "notes": "Customer birthday"
    }