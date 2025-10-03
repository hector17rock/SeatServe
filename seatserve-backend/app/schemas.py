"""
Pydantic schemas for request and response validation
"""
from pydantic import BaseModel, EmailStr, field_validator, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum


# Enums
class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY = "ready"
    SERVED = "served"
    PAID = "paid"
    CANCELLED = "cancelled"


class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class PaymentMethod(str, Enum):
    CASH = "cash"
    CARD = "card"
    DIGITAL = "digital"


class StaffRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    WAITER = "waiter"
    CHEF = "chef"
    CASHIER = "cashier"


# Base schemas
class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# Table schemas
class TableBase(BaseSchema):
    number: int
    capacity: int
    is_available: bool = True
    location: Optional[str] = None


class TableCreate(TableBase):
    pass


class TableUpdate(BaseSchema):
    number: Optional[int] = None
    capacity: Optional[int] = None
    is_available: Optional[bool] = None
    location: Optional[str] = None


class TableResponse(TableBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]


# Category schemas
class CategoryBase(BaseSchema):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    is_active: bool = True
    sort_order: int = 0


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None


class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]


# Menu item schemas
class MenuItemBase(BaseSchema):
    name: str
    description: Optional[str] = None
    price: float
    category_id: int
    is_available: bool = True
    image_url: Optional[str] = None
    ingredients: Optional[str] = None
    allergens: Optional[str] = None
    calories: Optional[int] = None
    preparation_time: Optional[int] = None
    is_vegetarian: bool = False
    is_vegan: bool = False
    is_gluten_free: bool = False
    sort_order: int = 0

    @field_validator('price')
    @classmethod
    def validate_price(cls, v):
        if v < 0:
            raise ValueError('Price must be positive')
        return round(v, 2)


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemUpdate(BaseSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None
    is_available: Optional[bool] = None
    image_url: Optional[str] = None
    ingredients: Optional[str] = None
    allergens: Optional[str] = None
    calories: Optional[int] = None
    preparation_time: Optional[int] = None
    is_vegetarian: Optional[bool] = None
    is_vegan: Optional[bool] = None
    is_gluten_free: Optional[bool] = None
    sort_order: Optional[int] = None

    @field_validator('price')
    @classmethod
    def validate_price(cls, v):
        if v is not None and v < 0:
            raise ValueError('Price must be positive')
        return round(v, 2) if v is not None else v


class MenuItemResponse(MenuItemBase):
    id: int
    category: Optional[CategoryResponse] = None
    created_at: datetime
    updated_at: Optional[datetime]


# Order item schemas
class OrderItemBase(BaseSchema):
    menu_item_id: int
    quantity: int = 1
    special_instructions: Optional[str] = None

    @field_validator('quantity')
    @classmethod
    def validate_quantity(cls, v):
        if v < 1:
            raise ValueError('Quantity must be at least 1')
        return v


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemUpdate(BaseSchema):
    quantity: Optional[int] = None
    special_instructions: Optional[str] = None
    status: Optional[str] = None


class OrderItemResponse(BaseSchema):
    id: int
    menu_item_id: int
    menu_item: Optional[MenuItemResponse] = None
    quantity: int
    unit_price: float
    total_price: float
    special_instructions: Optional[str]
    status: str
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


# Order schemas
class OrderBase(BaseSchema):
    table_id: int
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_email: Optional[EmailStr] = None
    notes: Optional[str] = None


class OrderCreate(OrderBase):
    items: List[OrderItemCreate] = []


class OrderUpdate(BaseSchema):
    table_id: Optional[int] = None
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_email: Optional[EmailStr] = None
    status: Optional[OrderStatus] = None
    notes: Optional[str] = None
    payment_method: Optional[PaymentMethod] = None
    payment_status: Optional[PaymentStatus] = None
    tip: Optional[float] = None


class OrderResponse(OrderBase):
    id: int
    status: OrderStatus
    subtotal: float
    tax: float
    tip: float
    total: float
    payment_method: Optional[PaymentMethod]
    payment_status: PaymentStatus
    table: Optional[TableResponse]
    order_items: List[OrderItemResponse] = []
    created_at: datetime
    updated_at: Optional[datetime]
    completed_at: Optional[datetime]


# Staff schemas
class StaffBase(BaseSchema):
    username: str
    email: EmailStr
    full_name: str
    role: StaffRole = StaffRole.WAITER
    is_active: bool = True
    phone: Optional[str] = None


class StaffCreate(StaffBase):
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v


class StaffUpdate(BaseSchema):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[StaffRole] = None
    is_active: Optional[bool] = None
    phone: Optional[str] = None
    password: Optional[str] = None


class StaffResponse(StaffBase):
    id: int
    hire_date: Optional[datetime]
    created_at: datetime
    last_login: Optional[datetime]


# Authentication schemas
class Token(BaseSchema):
    access_token: str
    token_type: str


class TokenData(BaseSchema):
    username: Optional[str] = None


class LoginRequest(BaseSchema):
    username: str
    password: str


# Restaurant schemas
class RestaurantBase(BaseSchema):
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    timezone: str = "UTC"
    currency: str = "USD"
    tax_rate: float = 0.0
    service_charge: float = 0.0
    opening_hours: Optional[str] = None
    is_open: bool = True


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantUpdate(BaseSchema):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    timezone: Optional[str] = None
    currency: Optional[str] = None
    tax_rate: Optional[float] = None
    service_charge: Optional[float] = None
    opening_hours: Optional[str] = None
    is_open: Optional[bool] = None


class RestaurantResponse(RestaurantBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]


# Response models
class MessageResponse(BaseSchema):
    message: str
    detail: Optional[str] = None


class PaginatedResponse(BaseSchema):
    items: List
    total: int
    page: int
    pages: int
    per_page: int
