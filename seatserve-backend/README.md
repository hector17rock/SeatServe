<div align="center">
  <img src="../Frontend/public/Images/seatserve-app-icon.png" alt="SeatServe Logo" width="120" height="120">
</div>

# SeatServe Backend

A robust FastAPI-based REST API for restaurant table service management with integrated Stripe payment processing. Built with Python, FastAPI, SQLite, and designed for high-performance real-time operations.

## Authors

**Héctor Soto**  
Backend Software Engineer  
GitHub: [@hector17rock](https://github.com/hector17rock)

**Alejandro Garcia**  
Backend Software Engineer  
GitHub: [@GerAle30](https://github.com/GerAle30)

## Overview

SeatServe Backend is a comprehensive API service that handles menu management, order processing, table management, and payment processing for restaurant and venue operations. The system features real-time logging, secure payment integration with Stripe, and a SQLite database for efficient data management.

## ✨ Features

### Core Functionality
- **Menu Management**: Full CRUD operations for menu items with category support
- **Order Processing**: Real-time order creation and tracking
- **Table Management**: Restaurant table status and availability management
- **Payment Processing**: Integrated Stripe payment system with webhooks

### Payment Integration
- **Stripe Payment Intents**: Secure payment processing
- **Payment Tracking**: Complete payment history and status management
- **Webhook Support**: Real-time payment event handling
- **Card Processing**: Support for Visa, Mastercard, Amex, and Discover

### API Features
- **RESTful Architecture**: Standard HTTP methods and status codes
- **Auto-generated Documentation**: Interactive Swagger UI and ReDoc
- **CORS Enabled**: Cross-origin resource sharing for frontend integration
- **Request Logging**: Comprehensive logging with emoji indicators
- **Error Handling**: Structured error responses with detail messages

### Database
- **SQLite**: Lightweight, file-based database
- **Schema Management**: Automatic table creation and initialization
- **Sample Data**: Pre-populated menu items and tables for testing
- **Foreign Keys**: Referential integrity for orders and payments

## 🛠 Tech Stack

### Core Technologies
- **FastAPI 0.104.1** - Modern, fast web framework
- **Uvicorn 0.24.0** - ASGI server with auto-reload
- **Python 3.8+** - Programming language
- **SQLite3** - Embedded database

### Key Libraries
- **Stripe** - Payment processing SDK
- **Pydantic 2.5.0** - Data validation and settings management
- **python-dotenv 1.0.0** - Environment variable management
- **python-jose 3.3.0** - JWT authentication support

### Middleware & CORS
- **CORSMiddleware** - Cross-origin request handling
- **LoggingMiddleware** - Custom request/response logging

### Development Tools
- **pytest 7.4.3** - Testing framework
- **Black 23.11.0** - Code formatting
- **Flake8 6.1.0** - Code linting
- **MyPy 1.7.1** - Static type checking

## 📁 Project Structure

```
seatserve-backend/
├── main.py                     # Main application entry point (672 lines)
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (DO NOT COMMIT)
├── .env.example               # Example environment configuration
├── STRIPE_SETUP.md            # Stripe integration guide
├── package.json               # Node package metadata
├── seatserve.db               # SQLite database file
├── seatserve_dev.db          # Development database
├── backend.log                # Application logs
├── test_main.py              # API tests
├── venv/                      # Virtual environment
├── __pycache__/              # Python cache
├── app/                       # Application modules
└── tests/                     # Test suite
```

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+** (Python 3.13 recommended)
- **pip** - Python package manager
- **Virtual environment** (recommended)
- **Stripe Account** - For payment processing

### Installation

1. **Navigate to backend directory:**
```bash
cd /Users/hector/SeatServe/seatserve-backend
```

2. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env and add your Stripe keys
```

### Configuration

**Edit `.env` file with your Stripe credentials:**

```bash
# Stripe API Keys
STRIPE_SECRET_KEY=sk_test_your_secret_key_here
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key_here

# Application Settings
APP_ENV=development
DATABASE_URL=sqlite:///seatserve.db
```

> **Important:** Get your Stripe keys from https://dashboard.stripe.com/test/apikeys

### Development

**Start the server:**
```bash
python3 main.py
```

The API will be available at **http://localhost:8000**

**Alternative (with uvicorn directly):**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Running in Background

```bash
python3 main.py > /tmp/seatserve_backend.log 2>&1 &
```

**Check logs:**
```bash
tail -f /tmp/seatserve_backend.log
```

## 📱 API Endpoints

### Root & Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome page with API information |
| GET | `/health` | Health check endpoint |
| GET | `/docs` | Interactive Swagger documentation |
| GET | `/redoc` | Alternative API documentation |

### Menu Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/menu` | Get all available menu items |
| GET | `/api/menu/categories` | Get all menu categories |
| POST | `/api/menu` | Create a new menu item |

**Example Menu Item:**
```json
{
  "name": "Margherita Pizza",
  "description": "Fresh tomato, mozzarella, basil",
  "price": 12.99,
  "category": "Mains",
  "available": true
}
```

### Order Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/orders` | Get all orders (sorted by timestamp) |
| POST | `/api/orders` | Create a new order |

**Example Order:**
```json
{
  "table_number": 5,
  "items": [
    {"id": "1", "name": "Pizza", "price": 12.99, "qty": 2}
  ],
  "total": 25.98,
  "status": "pending"
}
```

### Table Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tables` | Get all restaurant tables |
| PUT | `/api/tables/{table_id}/status` | Update table status |

**Table Statuses:**
- `available` - Table is free
- `occupied` - Table is in use
- `reserved` - Table is reserved

### Payment Processing

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/payments` | Get all payments |
| POST | `/api/payments` | Create a new payment record |
| PUT | `/api/payments/{id}/confirm` | Confirm/complete a payment |
| PUT | `/api/payments/{id}/reject` | Reject/cancel a payment |

### Stripe Integration

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/stripe/config` | Get Stripe publishable key |
| POST | `/api/stripe/create-payment-intent` | Create payment intent |
| POST | `/api/stripe/webhook` | Handle Stripe webhook events |

**Payment Intent Request:**
```json
{
  "amount": 27.85,
  "order_data": {
    "items": [...],
    "table_number": 5
  }
}
```

**Payment Intent Response:**
```json
{
  "clientSecret": "pi_xxxxx_secret_xxxxx",
  "paymentIntentId": "pi_xxxxx"
}
```

## 🎨 Database Schema

### Menu Items
```sql
CREATE TABLE menu_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    category TEXT NOT NULL,
    available BOOLEAN DEFAULT 1
)
```

### Orders
```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_number INTEGER NOT NULL,
    items TEXT NOT NULL,           -- JSON array
    total REAL NOT NULL,
    status TEXT DEFAULT 'pending',
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
)
```

### Restaurant Tables
```sql
CREATE TABLE restaurant_tables (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number INTEGER UNIQUE NOT NULL,
    seats INTEGER NOT NULL,
    status TEXT DEFAULT 'available'
)
```

### Payments
```sql
CREATE TABLE payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    payment_method TEXT DEFAULT 'card',
    status TEXT DEFAULT 'pending',
    transaction_id TEXT,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id)
)
```

## 🔧 Configuration

### CORS Settings

CORS is configured to allow all origins during development:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

> **Production Note:** Replace `["*"]` with specific frontend origins.

### Logging Configuration

Custom logging middleware logs all requests with emoji indicators:

- 📨 Incoming request
- 📦 Request body
- ✅ Successful response
- ❌ Error response
- 💳 Payment operation
- 🍽️ Menu operation
- 📋 Order operation
- 🪑 Table operation

## 📦 Dependencies

### Production Dependencies
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
python-dotenv==1.0.0
stripe (latest)
python-jose[cryptography]==3.3.0
python-multipart==0.0.6
passlib[bcrypt]==1.7.4
```

### Development Dependencies
```
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
black==23.11.0
flake8==6.1.0
mypy==1.7.1
```

## 🔐 Security Features

- **Environment Variables**: All sensitive data in `.env` file
- **Stripe SDK**: Official Stripe Python library for secure payments
- **HTTPS Ready**: Supports SSL/TLS in production
- **Input Validation**: Pydantic models validate all inputs
- **SQL Injection Protection**: Parameterized queries
- **Webhook Signatures**: Stripe webhook signature verification

## 🌐 API Documentation

Access interactive documentation at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Features:
- Try out endpoints directly
- View request/response schemas
- Authentication testing
- Example payloads

## 💳 Stripe Integration

### Setup Process

1. **Get API Keys** from Stripe Dashboard
2. **Add to `.env`** file
3. **Start server**
4. **Frontend automatically receives** publishable key

### Payment Flow

1. Frontend requests payment intent via `/api/stripe/create-payment-intent`
2. Backend creates Stripe Payment Intent
3. Frontend collects card details with Stripe Elements
4. Frontend confirms payment with Stripe
5. Stripe sends webhook to `/api/stripe/webhook`
6. Backend updates payment status

### Test Cards

| Card Number | Scenario |
|-------------|----------|
| `4242 4242 4242 4242` | Successful payment |
| `4000 0025 0000 3155` | Requires authentication |
| `4000 0000 0000 9995` | Card declined |

Use any future expiration date, any 3-digit CVV, and any 5-digit ZIP.

## 🐛 Troubleshooting

### Server Won't Start

**Port 8000 already in use:**
```bash
lsof -ti:8000 | xargs kill
```

**Missing dependencies:**
```bash
pip install -r requirements.txt
```

### Database Issues

**Database locked:**
```bash
rm seatserve.db
# Server will recreate with sample data
```

**Schema errors:**
- Delete database file
- Restart server to recreate schema

### Stripe Integration

**"Invalid API key":**
- Check `.env` file has correct keys
- Verify no extra spaces in keys
- Ensure using test keys (starts with `sk_test_`)

**Webhook signature verification fails:**
- Set `STRIPE_WEBHOOK_SECRET` in `.env`
- Or remove webhook secret for development

### CORS Errors

**Frontend can't connect:**
- Verify backend is running on port 8000
- Check CORS middleware configuration
- Ensure frontend uses correct backend URL

## 📝 Sample Data

The database initializes with sample data:

### Menu Items (8 items)
- Margherita Pizza ($12.99)
- Caesar Salad ($8.99)
- Grilled Salmon ($18.99)
- Chocolate Cake ($6.99)
- Coffee ($2.99)
- Burger Classic ($14.99)
- Greek Salad ($9.99)
- Tiramisu ($7.99)

### Tables (8 tables)
- Tables 1-8 with varying seat counts (2-8 seats)

## 🧪 Testing

**Run tests:**
```bash
pytest test_main.py -v
```

**Run with coverage:**
```bash
pytest test_main.py --cov=main --cov-report=html
```

**Test specific endpoint:**
```bash
pytest test_main.py::test_health_check -v
```

## 🚧 Future Enhancements

- [ ] User authentication with JWT
- [ ] PostgreSQL support for production
- [ ] Redis caching for menu items
- [ ] WebSocket support for real-time updates
- [ ] Order status notifications
- [ ] Admin dashboard API
- [ ] Rate limiting
- [ ] API versioning
- [ ] Comprehensive test coverage
- [ ] Docker containerization

## 📄 License

Demo MVP Project - All Rights Reserved © 2025 SeatServe

## 🤝 Related Projects

- **Frontend**: `/Users/hector/SeatServe/frontend/`
- **Django Models**: `/Users/hector/SeatServe/backend/`

## 📞 Support

For issues or questions:

1. Check the troubleshooting section
2. Review logs at `/tmp/seatserve_backend.log`
3. Check API documentation at http://localhost:8000/docs
4. Verify environment configuration in `.env`
5. Contact the development team

## 🔄 Environment Management

### Stop Server
```bash
# Find process
ps aux | grep "python.*main.py"

# Kill by PID
kill <PID>
```

### View Logs
```bash
# Real-time logs
tail -f /tmp/seatserve_backend.log

# Last 100 lines
tail -n 100 backend.log
```

### Database Management
```bash
# Backup database
cp seatserve.db seatserve.db.backup

# Reset database
rm seatserve.db && python3 main.py
```

---

**Status:** ✅ **COMPLETED**

Built with ❤️ by Héctor Soto & Alejandro Garcia
