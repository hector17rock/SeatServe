"""
Utility functions for SeatServe API
"""
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import logging
from app.config import settings

logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    
    return encoded_jwt


def verify_token(token: str) -> Optional[str]:
    """Verify JWT token and return username"""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError as e:
        logger.warning(f"Token verification failed: {e}")
        return None


def calculate_order_total(subtotal: float, tax_rate: float = 0.0, tip: float = 0.0, service_charge: float = 0.0) -> dict:
    """Calculate order totals including tax, tip, and service charge"""
    tax = round(subtotal * tax_rate, 2)
    service = round(subtotal * service_charge, 2)
    total = round(subtotal + tax + service + tip, 2)
    
    return {
        "subtotal": subtotal,
        "tax": tax,
        "service_charge": service,
        "tip": tip,
        "total": total
    }


def format_currency(amount: float, currency: str = "USD") -> str:
    """Format amount as currency string"""
    currency_symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥"
    }
    
    symbol = currency_symbols.get(currency, currency)
    return f"{symbol}{amount:.2f}"


def generate_order_number() -> str:
    """Generate unique order number"""
    from datetime import datetime
    now = datetime.now()
    return f"ORD{now.strftime('%Y%m%d%H%M%S')}"


def validate_email(email: str) -> bool:
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """Basic phone number validation"""
    import re
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    # Check if it has 10-15 digits (international format)
    return len(digits_only) >= 10 and len(digits_only) <= 15


def sanitize_string(text: str) -> str:
    """Sanitize string input"""
    if not text:
        return ""
    # Remove extra whitespace
    return " ".join(text.strip().split())


def get_pagination_params(page: int = 1, per_page: int = 20) -> dict:
    """Get pagination parameters"""
    page = max(1, page)
    per_page = max(1, min(100, per_page))  # Limit to 100 items per page
    offset = (page - 1) * per_page
    
    return {
        "offset": offset,
        "limit": per_page,
        "page": page,
        "per_page": per_page
    }


def calculate_pagination_info(total_items: int, page: int, per_page: int) -> dict:
    """Calculate pagination information"""
    total_pages = (total_items + per_page - 1) // per_page
    
    return {
        "total": total_items,
        "page": page,
        "pages": total_pages,
        "per_page": per_page,
        "has_next": page < total_pages,
        "has_prev": page > 1
    }


class OrderCalculator:
    """Helper class for order calculations"""
    
    def __init__(self, tax_rate: float = 0.0, service_charge: float = 0.0):
        self.tax_rate = tax_rate
        self.service_charge = service_charge
    
    def calculate_item_total(self, unit_price: float, quantity: int) -> float:
        """Calculate total for an order item"""
        return round(unit_price * quantity, 2)
    
    def calculate_subtotal(self, items: list) -> float:
        """Calculate subtotal from list of items"""
        subtotal = sum(item.get('total_price', 0) for item in items)
        return round(subtotal, 2)
    
    def calculate_totals(self, subtotal: float, tip: float = 0.0) -> dict:
        """Calculate all totals for an order"""
        return calculate_order_total(
            subtotal=subtotal,
            tax_rate=self.tax_rate,
            tip=tip,
            service_charge=self.service_charge
        )


def log_activity(action: str, user_id: Optional[int] = None, details: Optional[dict] = None):
    """Log user activity"""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "action": action,
        "user_id": user_id,
        "details": details or {}
    }
    logger.info(f"Activity: {log_entry}")


def handle_database_error(error: Exception, operation: str) -> str:
    """Handle database errors and return user-friendly message"""
    error_msg = str(error)
    logger.error(f"Database error during {operation}: {error_msg}")
    
    if "duplicate key" in error_msg.lower():
        return "A record with this information already exists"
    elif "foreign key" in error_msg.lower():
        return "Referenced record does not exist"
    elif "not null" in error_msg.lower():
        return "Required information is missing"
    else:
        return "Database operation failed"
