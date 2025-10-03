# SeatServe Backend API

A comprehensive REST API for restaurant table service management built with FastAPI and PostgreSQL.

## Features

- **Menu Management**: Categories and menu items with detailed information
- **Order Processing**: Complete order lifecycle management
- **Table Management**: Table availability and assignment
- **Staff Authentication**: Role-based access control
- **Real-time Updates**: Order status tracking
- **Comprehensive Validation**: Pydantic schemas for data validation
- **Database Migrations**: SQLAlchemy ORM with Alembic
- **API Documentation**: Auto-generated with FastAPI

## Architecture

```
seatserve-backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── db.py                # Database connection and session management
│   ├── models.py            # SQLAlchemy database models
│   ├── schemas.py           # Pydantic validation schemas
│   ├── utils.py             # Utility functions
│   ├── __init__.py
│   └── routers/
│       ├── menu.py          # Menu management endpoints
│       ├── orders.py        # Order management endpoints
│       └── __init__.py
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore file
└── README.md               # This file
```

## Requirements

- Python 3.8+
- PostgreSQL 12+
- Virtual environment (recommended)

## Quick Start

### 1. Clone and Setup

```bash
cd seatserve-backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Configuration

```bash
cp .env.example .env
# Edit .env file with your database credentials and settings
```

### 3. Database Setup

```bash
# Create PostgreSQL database
createdb seatserve_db

# Update DATABASE_URL in .env file
DATABASE_URL=postgresql://username:password@localhost:5432/seatserve_db
```

### 4. Run the Application

```bash
# Development mode
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using Python
python app/main.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## Database Models

### Core Models

- **Restaurant**: Restaurant configuration and settings
- **Table**: Restaurant tables with capacity and location
- **Category**: Menu categories (Appetizers, Main Courses, etc.)
- **MenuItem**: Individual menu items with pricing and details
- **Order**: Customer orders with status tracking
- **OrderItem**: Individual items within an order
- **Staff**: Staff members with role-based access

### Relationships

- Categories → MenuItems (one-to-many)
- Tables → Orders (one-to-many)
- Orders → OrderItems (one-to-many)
- MenuItems → OrderItems (one-to-many)

## API Endpoints

### Menu Management

```
GET    /api/v1/menu/categories           # List categories
POST   /api/v1/menu/categories           # Create category
GET    /api/v1/menu/categories/{id}      # Get category
PUT    /api/v1/menu/categories/{id}      # Update category
DELETE /api/v1/menu/categories/{id}      # Delete category

GET    /api/v1/menu/items                # List menu items
POST   /api/v1/menu/items                # Create menu item
GET    /api/v1/menu/items/{id}           # Get menu item
PUT    /api/v1/menu/items/{id}           # Update menu item
DELETE /api/v1/menu/items/{id}           # Delete menu item
PATCH  /api/v1/menu/items/{id}/availability # Toggle availability

GET    /api/v1/menu/categories/{id}/items # Get items by category
```

### Order Management

```
GET    /api/v1/orders                    # List orders
POST   /api/v1/orders                    # Create order
GET    /api/v1/orders/{id}               # Get order
PUT    /api/v1/orders/{id}               # Update order
DELETE /api/v1/orders/{id}               # Cancel order

POST   /api/v1/orders/{id}/items         # Add item to order
DELETE /api/v1/orders/{id}/items/{item_id} # Remove item from order
PATCH  /api/v1/orders/{id}/status        # Update order status

GET    /api/v1/orders/table/{table_id}/active # Get active order by table
```

### System Endpoints

```
GET    /                                 # Root endpoint
GET    /health                          # Health check
GET    /api/v1/info                     # API information
```

## Example Usage

### Create a Menu Category

```bash
curl -X POST "http://localhost:8000/api/v1/menu/categories" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Appetizers",
    "description": "Delicious starters to begin your meal",
    "is_active": true,
    "sort_order": 1
  }'
```

### Create a Menu Item

```bash
curl -X POST "http://localhost:8000/api/v1/menu/items" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Caesar Salad",
    "description": "Fresh romaine lettuce with parmesan and croutons",
    "price": 12.99,
    "category_id": 1,
    "is_available": true,
    "is_vegetarian": true,
    "calories": 320,
    "preparation_time": 10
  }'
```

### Create an Order

```bash
curl -X POST "http://localhost:8000/api/v1/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "table_id": 1,
    "customer_name": "John Doe",
    "customer_phone": "+1234567890",
    "items": [
      {
        "menu_item_id": 1,
        "quantity": 2,
        "special_instructions": "No croutons please"
      }
    ],
    "notes": "Customer allergic to gluten"
  }'
```

## Configuration

Key environment variables:

```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/seatserve_db

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
DEBUG=True
HOST=0.0.0.0
PORT=8000

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

## Development

### Code Structure

- **models.py**: SQLAlchemy ORM models
- **schemas.py**: Pydantic validation schemas
- **routers/**: API endpoint definitions
- **utils.py**: Utility functions and helpers
- **config.py**: Application configuration
- **db.py**: Database connection management

### Adding New Features

1. Define database model in `models.py`
2. Create Pydantic schemas in `schemas.py`
3. Implement endpoints in appropriate router
4. Add any utility functions to `utils.py`
5. Update documentation

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

## Deployment

### Docker (Recommended)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ ./app/
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Considerations

- Use environment variables for all configuration
- Enable HTTPS in production
- Set up proper logging
- Use a production ASGI server (Gunicorn + Uvicorn)
- Implement rate limiting
- Set up monitoring and health checks

## API Documentation

Once the server is running, visit:

- **Interactive Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions:

- Create an issue in the GitHub repository
- Check the API documentation at `/docs`
- Review the example usage above

## Status Codes

The API uses standard HTTP status codes:

- `200` - Success
- `201` - Created
- `400` - Bad Request (validation error)
- `404` - Not Found
- `422` - Unprocessable Entity
- `500` - Internal Server Error

Error responses include detailed messages:

```json
{
  "error": true,
  "message": "Menu item not found",
  "status_code": 404
}
```