"""
Tests for utility functions
"""
import pytest
from datetime import datetime, timedelta

from app.utils import (
    hash_password, verify_password, create_access_token, verify_token,
    calculate_order_total, format_currency, validate_email, validate_phone,
    sanitize_string, get_pagination_params, calculate_pagination_info,
    OrderCalculator
)


class TestPasswordUtils:
    """Test password hashing and verification"""
    
    def test_hash_password(self):
        """Test password hashing"""
        password = "testpassword123"
        hashed = hash_password(password)
        
        assert hashed != password
        assert len(hashed) > 20  # Bcrypt hashes are long
        assert hashed.startswith("$2b$")  # Bcrypt format
    
    def test_verify_password_correct(self):
        """Test password verification with correct password"""
        password = "testpassword123"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True
    
    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password"""
        password = "testpassword123"
        wrong_password = "wrongpassword"
        hashed = hash_password(password)
        
        assert verify_password(wrong_password, hashed) is False


class TestJWTUtils:
    """Test JWT token functions"""
    
    def test_create_access_token(self):
        """Test JWT token creation"""
        data = {"sub": "testuser"}
        token = create_access_token(data)
        
        assert isinstance(token, str)
        assert len(token) > 50  # JWT tokens are long
        assert "." in token  # JWT format has dots
    
    def test_create_access_token_with_expiry(self):
        """Test JWT token creation with custom expiry"""
        data = {"sub": "testuser"}
        expires_delta = timedelta(minutes=15)
        token = create_access_token(data, expires_delta)
        
        assert isinstance(token, str)
        # Token should still be valid
        username = verify_token(token)
        assert username == "testuser"
    
    def test_verify_token_valid(self):
        """Test JWT token verification with valid token"""
        data = {"sub": "testuser"}
        token = create_access_token(data)
        
        username = verify_token(token)
        assert username == "testuser"
    
    def test_verify_token_invalid(self):
        """Test JWT token verification with invalid token"""
        invalid_token = "invalid.token.here"
        
        username = verify_token(invalid_token)
        assert username is None


class TestOrderCalculations:
    """Test order calculation functions"""
    
    def test_calculate_order_total_no_extras(self):
        """Test order total calculation with no tax or tip"""
        result = calculate_order_total(100.0)
        
        assert result["subtotal"] == 100.0
        assert result["tax"] == 0.0
        assert result["service_charge"] == 0.0
        assert result["tip"] == 0.0
        assert result["total"] == 100.0
    
    def test_calculate_order_total_with_tax(self):
        """Test order total calculation with tax"""
        result = calculate_order_total(100.0, tax_rate=0.08)
        
        assert result["subtotal"] == 100.0
        assert result["tax"] == 8.0
        assert result["total"] == 108.0
    
    def test_calculate_order_total_with_all_extras(self):
        """Test order total calculation with tax, tip, and service charge"""
        result = calculate_order_total(100.0, tax_rate=0.08, tip=15.0, service_charge=0.05)
        
        assert result["subtotal"] == 100.0
        assert result["tax"] == 8.0
        assert result["service_charge"] == 5.0
        assert result["tip"] == 15.0
        assert result["total"] == 128.0


class TestCurrencyFormatting:
    """Test currency formatting"""
    
    def test_format_currency_usd(self):
        """Test USD currency formatting"""
        result = format_currency(12.99, "USD")
        assert result == "$12.99"
    
    def test_format_currency_eur(self):
        """Test EUR currency formatting"""
        result = format_currency(12.99, "EUR")
        assert result == "€12.99"
    
    def test_format_currency_unknown(self):
        """Test unknown currency formatting"""
        result = format_currency(12.99, "XYZ")
        assert result == "XYZ12.99"
    
    def test_format_currency_rounding(self):
        """Test currency formatting with rounding"""
        result = format_currency(12.999, "USD")
        assert result == "$13.00"


class TestValidationUtils:
    """Test validation utility functions"""
    
    def test_validate_email_valid(self):
        """Test email validation with valid emails"""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "user+tag@example.org"
        ]
        
        for email in valid_emails:
            assert validate_email(email) is True
    
    def test_validate_email_invalid(self):
        """Test email validation with invalid emails"""
        invalid_emails = [
            "notanemail",
            "@domain.com",
            "user@",
            "user space@domain.com"
        ]
        
        for email in invalid_emails:
            assert validate_email(email) is False
    
    def test_validate_phone_valid(self):
        """Test phone validation with valid numbers"""
        valid_phones = [
            "+1234567890",
            "123-456-7890",
            "(123) 456-7890",
            "1234567890"
        ]
        
        for phone in valid_phones:
            assert validate_phone(phone) is True
    
    def test_validate_phone_invalid(self):
        """Test phone validation with invalid numbers"""
        invalid_phones = [
            "123",
            "abc-def-ghij",
            "+123456789012345678"  # Too long
        ]
        
        for phone in invalid_phones:
            assert validate_phone(phone) is False
    
    def test_sanitize_string(self):
        """Test string sanitization"""
        assert sanitize_string("  hello   world  ") == "hello world"
        assert sanitize_string("") == ""
        assert sanitize_string(None) == ""
        assert sanitize_string("normal text") == "normal text"


class TestPaginationUtils:
    """Test pagination utility functions"""
    
    def test_get_pagination_params_defaults(self):
        """Test pagination parameters with defaults"""
        result = get_pagination_params()
        
        assert result["page"] == 1
        assert result["per_page"] == 20
        assert result["offset"] == 0
        assert result["limit"] == 20
    
    def test_get_pagination_params_custom(self):
        """Test pagination parameters with custom values"""
        result = get_pagination_params(page=3, per_page=10)
        
        assert result["page"] == 3
        assert result["per_page"] == 10
        assert result["offset"] == 20  # (3-1) * 10
        assert result["limit"] == 10
    
    def test_get_pagination_params_bounds(self):
        """Test pagination parameters boundary conditions"""
        # Test minimum bounds
        result = get_pagination_params(page=0, per_page=0)
        assert result["page"] == 1
        assert result["per_page"] == 1
        
        # Test maximum bounds
        result = get_pagination_params(per_page=200)
        assert result["per_page"] == 100  # Max limit
    
    def test_calculate_pagination_info(self):
        """Test pagination information calculation"""
        result = calculate_pagination_info(total_items=50, page=2, per_page=10)
        
        assert result["total"] == 50
        assert result["page"] == 2
        assert result["pages"] == 5
        assert result["per_page"] == 10
        assert result["has_next"] is True
        assert result["has_prev"] is True
    
    def test_calculate_pagination_info_edge_cases(self):
        """Test pagination information edge cases"""
        # First page
        result = calculate_pagination_info(total_items=50, page=1, per_page=10)
        assert result["has_prev"] is False
        assert result["has_next"] is True
        
        # Last page
        result = calculate_pagination_info(total_items=50, page=5, per_page=10)
        assert result["has_prev"] is True
        assert result["has_next"] is False
        
        # No items
        result = calculate_pagination_info(total_items=0, page=1, per_page=10)
        assert result["pages"] == 0


class TestOrderCalculatorClass:
    """Test OrderCalculator helper class"""
    
    def test_calculate_item_total(self):
        """Test item total calculation"""
        calculator = OrderCalculator()
        
        total = calculator.calculate_item_total(12.99, 2)
        assert total == 25.98
    
    def test_calculate_subtotal(self):
        """Test subtotal calculation from items"""
        calculator = OrderCalculator()
        
        items = [
            {"total_price": 12.99},
            {"total_price": 8.50},
            {"total_price": 15.75}
        ]
        
        subtotal = calculator.calculate_subtotal(items)
        assert subtotal == 37.24
    
    def test_calculate_totals_with_rates(self):
        """Test total calculation with tax and service rates"""
        calculator = OrderCalculator(tax_rate=0.08, service_charge=0.05)
        
        totals = calculator.calculate_totals(subtotal=100.0, tip=10.0)
        
        assert totals["subtotal"] == 100.0
        assert totals["tax"] == 8.0
        assert totals["service_charge"] == 5.0
        assert totals["tip"] == 10.0
        assert totals["total"] == 123.0