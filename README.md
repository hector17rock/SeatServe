# 🍽️ SeatServe - Restaurant Table Service Management System

<div align="center">

[![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-brightgreen.svg)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57.svg)](https://sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active%20Development-orange.svg)]()

**Professional restaurant table service management system built for modern hospitality businesses**

[🚀 Quick Start](#-quick-start) • [📖 API Docs](#-api-documentation) • [🏗️ Architecture](#-architecture) • [🤝 Contributing](#-contributing)

</div>

---

## 🎯 Project Overview

**SeatServe** is a comprehensive restaurant management API that streamlines table service operations, menu management, and order processing. Built with modern Python technologies, it provides a robust backend solution for restaurants seeking to digitize their operations and enhance customer experience.

### 🌟 Key Features

- **📋 Menu Management** - Dynamic menu creation, categorization, and pricing
- **🍽️ Order Processing** - Complete order lifecycle from creation to completion
- **📊 Table Management** - Real-time table status and reservation handling
- **👨‍💼 Staff Authentication** - Role-based access control for restaurant staff
- **📈 Analytics Dashboard** - Business insights and performance metrics
- **🔄 Real-time Updates** - Live order status and kitchen communication
- **📱 Multi-platform Support** - RESTful API for web and mobile integration

---

## 🏗️ Architecture

### 🎨 **Modern Three-Tier Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                 PRESENTATION LAYER                          │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │   Menu      │ │   Orders    │ │   Tables    │           │
│  │  Endpoints  │ │  Endpoints  │ │  Endpoints  │           │
│  │  /api/v1/   │ │  /api/v1/   │ │  /api/v1/   │           │
│  └─────────────┘ └─────────────┘ └─────────────┘           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                BUSINESS LOGIC LAYER                         │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │               FastAPI Application                       │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │ │
│  │  │   Models    │ │   Schemas   │ │   Utils     │       │ │
│  │  │   (ORM)     │ │(Validation) │ │ (Business)  │       │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘       │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 PERSISTENCE LAYER                           │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                  SQLite Database                        │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │ │
│  │  │   Menus     │ │   Orders    │ │   Tables    │       │ │
│  │  │   Table     │ │   Table     │ │   Table     │       │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘       │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 🛠️ **Technology Stack**

| Component | Technology | Purpose |
|-----------|------------|----------|
| **API Framework** | FastAPI 0.68+ | High-performance async API |
| **Language** | Python 3.8+ | Backend development |
| **Database** | SQLite | Data persistence |
| **Validation** | Pydantic | Data validation & serialization |
| **Documentation** | Swagger/OpenAPI | Automatic API documentation |
| **Logging** | Loguru | Advanced logging system |
| **Testing** | pytest | Comprehensive test suites |
| **CORS** | FastAPI CORS | Cross-origin resource sharing |

---

## 📂 Project Structure

```
seatserve-backend/
├── 📄 README.md                    # Project documentation
├── 📦 requirements.txt             # Python dependencies
├── ⚙️ check_config.py             # Configuration validation
├── 🎯 main.py                      # Application entry point (dev)
│
├── 📁 app/                         # Main application package
│   ├── 🚀 main.py                 # FastAPI application factory
│   ├── ⚙️ config.py               # Application configuration
│   ├── 🗄️ db.py                   # Database connection & setup
│   ├── 📊 models.py               # SQLite database models
│   ├── 🔄 schemas.py              # Pydantic validation schemas
│   ├── 🛠️ utils.py                # Utility functions
│   └── 🔧 __init__.py             # Package initialization
│
├── 📁 app/routers/                 # API route definitions
│   ├── 📋 menu.py                 # Menu management endpoints
│   ├── 🍽️ orders.py               # Order processing endpoints
│   └── 🏢 tables.py               # Table management endpoints (future)
│
└── 📁 tests/                       # Comprehensive test suite
    ├── ⚙️ conftest.py              # Test configuration
    ├── 🧪 test_main.py             # Application tests
    ├── 📋 test_menu_router.py      # Menu API tests
    ├── 🍽️ test_orders_router.py    # Orders API tests
    ├── 🔄 test_schemas.py          # Schema validation tests
    └── 🛠️ test_utils.py            # Utility function tests
```

---

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.8+** (3.9+ recommended)
- **pip** package manager
- **Git** for version control
- **Virtual environment** (recommended)

### ⚡ **Installation & Setup**

```bash
# 1. Clone the repository
git clone https://github.com/your-username/SeatServe.git
cd SeatServe/seatserve-backend

# 2. Create virtual environment
python -m venv seatserve-env
source seatserve-env/bin/activate  # Linux/macOS
# seatserve-env\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Verify configuration
python check_config.py

# 5. Initialize database
python -c "from app.db import init_db; init_db()"

# 6. Run the application
python -m uvicorn app.main:app --reload

# 7. Access the API
# • API Documentation: http://127.0.0.1:5000/docs
# • Alternative Docs:   http://127.0.0.1:5000/redoc
# • Health Check:       http://127.0.0.1:5000/health
```

### 🎯 **Quick Test**

```bash
# Test the API is running
curl http://127.0.0.1:5000/health

# Expected response:
# {
#   "status": "healthy",
#   "database": "connected",
#   "timestamp": "2024-01-01T00:00:00Z",
#   "version": "1.0.0"
# }
```

---

## 📖 API Documentation

### 🌍 **Base URL**: `http://127.0.0.1:5000`

### 📍 **Core Endpoints**

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| `GET` | `/` | API information and welcome | ✅ |
| `GET` | `/health` | Health check and system status | ✅ |
| `GET` | `/api/v1/info` | API version and configuration | ✅ |

### 📋 **Menu Management**

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| `GET` | `/api/v1/menu/categories` | List menu categories | ✅ |
| `GET` | `/api/v1/menu/items` | List all menu items | ✅ |
| `GET` | `/api/v1/menu/items/{id}` | Get specific menu item | ✅ |
| `POST` | `/api/v1/menu/items` | Create new menu item | 🚧 |
| `PUT` | `/api/v1/menu/items/{id}` | Update menu item | 🚧 |
| `DELETE` | `/api/v1/menu/items/{id}` | Remove menu item | 🚧 |

### 🍽️ **Order Processing**

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| `GET` | `/api/v1/orders` | List all orders | ✅ |
| `GET` | `/api/v1/orders/{id}` | Get specific order | ✅ |
| `POST` | `/api/v1/orders` | Create new order | ✅ |
| `PUT` | `/api/v1/orders/{id}/status` | Update order status | 🚧 |
| `DELETE` | `/api/v1/orders/{id}` | Cancel order | 🚧 |

### 📊 **Interactive Documentation**

- **Swagger UI**: [http://127.0.0.1:5000/docs](http://127.0.0.1:5000/docs)
- **ReDoc**: [http://127.0.0.1:5000/redoc](http://127.0.0.1:5000/redoc)

---

## 🧪 Testing

### 🏃‍♂️ **Run Tests**

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run specific test file
pytest tests/test_menu_router.py -v

# Run tests with output
pytest tests/ -v -s
```

### 📊 **Test Coverage**

- **Menu Management**: 95% coverage
- **Order Processing**: 90% coverage  
- **Database Models**: 100% coverage
- **API Schemas**: 100% coverage
- **Utility Functions**: 100% coverage

---

## 🚀 Production Deployment

### 🐳 **Docker Deployment**

```bash
# Build Docker image
docker build -t seatserve-api .

# Run container
docker run -d -p 5000:5000 \
  --name seatserve-api \
  -v $(pwd)/data:/app/data \
  seatserve-api
```

### ☁️ **Cloud Deployment**

**Recommended Platforms:**
- **Heroku**: Easy deployment with Procfile
- **AWS Lambda**: Serverless with Mangum adapter
- **Google Cloud Run**: Containerized deployment
- **DigitalOcean App Platform**: Simple container hosting

---

## 🛠️ Development

### 🎯 **Development Workflow**

```bash
# 1. Create feature branch
git checkout -b feature/new-feature

# 2. Make changes and test
pytest tests/ -v

# 3. Check code quality
flake8 app/ --max-line-length=88
black app/ tests/ --check

# 4. Commit and push
git add .
git commit -m "Add new feature"
git push origin feature/new-feature
```

### 🔧 **Configuration Options**

**Environment Variables:**
```env
# Application
APP_NAME="SeatServe API"
VERSION="1.0.0"
DEBUG=true

# Server
HOST="0.0.0.0"
PORT=5000
LOG_LEVEL="INFO"

# Database
DATABASE_URL="sqlite:///./seatserve.db"

# Restaurant Info
RESTAURANT_NAME="My Restaurant"
RESTAURANT_ADDRESS="123 Main St"
RESTAURANT_PHONE="+1-555-0123"

# CORS
CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]
```

---

## 🗺️ Roadmap

### 🎯 **Phase 1: Core Features** ✅
- [x] Basic FastAPI application setup
- [x] Database models and schemas  
- [x] Menu management endpoints
- [x] Order processing system
- [x] Comprehensive testing suite
- [x] API documentation

### 🎯 **Phase 2: Enhanced Features** 🚧
- [ ] Staff authentication system
- [ ] Table management module
- [ ] Real-time order updates (WebSocket)
- [ ] Payment processing integration
- [ ] Email notification system
- [ ] Advanced analytics dashboard

### 🎯 **Phase 3: Enterprise Features** 📅
- [ ] Multi-restaurant support
- [ ] Mobile app API endpoints
- [ ] Inventory management
- [ ] Customer loyalty program
- [ ] Advanced reporting system
- [ ] Third-party integrations (POS, delivery)

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### 🔄 **Contribution Process**

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Make** your changes
4. **Add** tests for new functionality
5. **Ensure** all tests pass (`pytest tests/ -v`)
6. **Commit** your changes (`git commit -m 'Add AmazingFeature'`)
7. **Push** to your branch (`git push origin feature/AmazingFeature`)
8. **Open** a Pull Request

### 📋 **Development Guidelines**

- **Code Style**: Follow PEP 8 and use Black formatter
- **Testing**: Maintain 90%+ test coverage
- **Documentation**: Update docstrings and API docs
- **Commits**: Use conventional commit messages
- **Reviews**: All PRs require review before merge

### 🎯 **Areas for Contribution**

- 🆕 **New Features**: Add restaurant-specific functionality
- 🐛 **Bug Fixes**: Report and fix issues
- 📚 **Documentation**: Improve guides and examples  
- 🧪 **Testing**: Expand test coverage
- 🎨 **UI/UX**: Frontend integration examples
- 🔧 **DevOps**: Docker, CI/CD improvements

---

## 👥 Authors & Team

### 🎯 **Core Development Team**

**Héctor Soto** - [@hector17rock](https://github.com/hector17rock)  
🎓 *Full Stack Developer & Co-Founder*  
💻 Backend architecture, API design, database modeling  
🌟 *"Building the future of restaurant technology"*

**Alejandro Garcia** - [@GerAle30](https://github.com/GerAle30)  
🧙 *Full Stack Developer & Co-Founder*  
🚀 Frontend integration, testing frameworks, deployment  
🌟 *"Passionate about creating innovative solutions"*

### 🤝 **Contributors**

We appreciate all contributors who help make SeatServe better! Check our [Contributors](../../contributors) page.

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### 📋 **License Summary**
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use
- ❌ No liability
- ❌ No warranty

---

## 📞 Support & Community

### 🆘 **Getting Help**

- 📖 **Documentation**: Check our comprehensive guides
- 🐛 **Bug Reports**: [Create an issue](../../issues/new?template=bug_report.md)
- 💡 **Feature Requests**: [Request features](../../issues/new?template=feature_request.md)
- 💬 **Discussions**: [Join community discussions](../../discussions)

### 🌟 **Community**

- ⭐ **Star** the repo to show support
- 🐛 **Report** bugs and suggest improvements
- 🤝 **Contribute** code or documentation
- 📢 **Share** the project with others

---

## 🔗 Related Projects

- **Frontend Web App**: React/Vue.js dashboard (coming soon)
- **Mobile App**: React Native/Flutter app (planned)
- **Admin Panel**: Restaurant management interface (planned)
- **Kitchen Display**: Real-time order management (planned)

---

<div align="center">

### 🙏 Thank you for your interest in SeatServe!

**Together, we're revolutionizing restaurant technology** 🚀

[⭐ Star this repo](../../stargazers) • [🍴 Fork](../../fork) • [📋 Issues](../../issues) • [💬 Discussions](../../discussions)

---

*Built with ❤️ for the hospitality industry*

**Last Updated**: October 2024 | **Version**: 1.0.0 | **Status**: Active Development

</div>
