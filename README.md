<div align="center">
  <img src="Frontend/public/Images/seatserve-app-icon.png" alt="SeatServe Logo" width="150" height="150">
</div>

# SeatServe

**A modern stadium and venue food ordering platform with seat delivery, integrated payment processing, and real-time order management.**

<div align="center">

[![Status](https://img.shields.io/badge/Status-MVP%20Complete-success)]() 
[![Frontend](https://img.shields.io/badge/Frontend-Vite%20%2B%20React-blue)]() 
[![Backend](https://img.shields.io/badge/Backend-FastAPI-green)]() 
[![Payment](https://img.shields.io/badge/Payment-Stripe-blueviolet)]()

</div>

## 👨‍💻 Authors

**Héctor Soto**  
Frontend Software Engineer  
GitHub: [@hector17rock](https://github.com/hector17rock)

**Alejandro Garcia**  
Backend Software Engineer  
GitHub: [@GerAle30](https://github.com/GerAle30)

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
- [Project Components](#project-components)
- [Documentation](#documentation)
- [License](#license)

## 🎯 Overview

SeatServe is a comprehensive food ordering platform designed for stadiums, venues, and restaurants. The system allows customers to browse menus from multiple concession stands, place orders, and complete secure payments through Stripe integration. Orders can be delivered directly to the customer's seat or picked up at the concession stand.

### Key Highlights

- 🍕 **Multi-Vendor System** - Support for multiple concession stands
- 💳 **Stripe Payments** - Secure, PCI-compliant payment processing
- 📱 **Responsive Design** - Beautiful UI for mobile, tablet, and desktop
- 🔐 **User Authentication** - Sign up, login, or continue as guest
- 📊 **Order Management** - Complete order tracking and management
- ⚡ **Real-time Updates** - Live cart management and order status

## 📁 Project Structure

```
SeatServe/
├── Frontend/                   # React + Vite frontend application
│   ├── public/                # Static assets and images
│   ├── src/                   # React components and pages
│   ├── index.html             # Login page
│   ├── concessions.html       # Concession selection
│   ├── checkout.html          # Payment page
│   ├── order_review.html      # Order confirmation
│   ├── package.json           # Frontend dependencies
│   └── README.md              # Frontend documentation
│
├── seatserve-backend/         # FastAPI backend (Active)
│   ├── main.py                # FastAPI application
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # Environment variables
│   ├── seatserve_dev.db       # SQLite database
│   └── README.md              # Backend documentation
│
├── backend/                   # Django models (Future use)
│   ├── app/
│   │   └── models/
│   │       └── payment.py     # Payment models
│   └── README.md              # Django models documentation
│
└── README.md                  # This file
```

## ✨ Features

### Customer Features
- **Browse Concessions** - View multiple vendor options with logos and operating hours
- **Menu Navigation** - Explore categorized menus with prices and descriptions
- **Shopping Cart** - Add/remove items with quantity selection
- **Guest Checkout** - Order without creating an account
- **User Accounts** - Sign up and login for faster checkout
- **Secure Payments** - Credit card processing via Stripe
- **Order Confirmation** - Clear confirmation with order details

### Payment Features
- **Stripe Integration** - Industry-standard payment processing
- **Multiple Card Types** - Visa, Mastercard, Amex, Discover
- **Card Validation** - Real-time validation and error handling
- **Billing Address** - Complete billing information collection
- **Receipt Generation** - Automatic receipt creation

### Technical Features
- **RESTful API** - Standard HTTP methods and status codes
- **CORS Support** - Cross-origin resource sharing enabled
- **Database Persistence** - SQLite for development
- **Logging System** - Comprehensive request/response logging
- **Error Handling** - Structured error responses

## 🛠 Technology Stack

### Frontend
- **Framework**: Vite 5.0.8 + React 18.2.0
- **Styling**: Tailwind CSS 3.3.6
- **Payment UI**: Stripe Elements
- **State Management**: localStorage + React state
- **Build Tool**: Vite with HMR
- **Linting**: ESLint

### Backend (FastAPI)
- **Framework**: FastAPI 0.104.1
- **Server**: Uvicorn 0.24.0
- **Database**: SQLite3
- **Payment Processing**: Stripe Python SDK
- **Validation**: Pydantic 2.5.0
- **Environment**: python-dotenv 1.0.0

### Backend (Django Models - Future)
- **ORM**: Django Models
- **Purpose**: Payment and transaction models
- **Status**: Not currently active

## 🚀 Getting Started

### Prerequisites

- **Node.js** 16+ (for frontend)
- **Python** 3.8+ (for backend)
- **npm** or **yarn**
- **Stripe Account** (for payments)

### Quick Start

#### 1. Clone the Repository
```bash
git clone https://github.com/hector17rock/SeatServe.git
cd SeatServe
```

#### 2. Start Backend Server
```bash
cd seatserve-backend
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your Stripe keys
python3 main.py
```

Backend runs on **http://localhost:8000**

#### 3. Start Frontend Server
```bash
cd Frontend
npm install
npm run dev
```

Frontend runs on **http://localhost:3000**

#### 4. Configure Stripe

1. Get API keys from [Stripe Dashboard](https://dashboard.stripe.com/test/apikeys)
2. Add keys to `seatserve-backend/.env`:
   ```
   STRIPE_SECRET_KEY=sk_test_your_key_here
   STRIPE_PUBLISHABLE_KEY=pk_test_your_key_here
   ```

### Test the Application

1. Open **http://localhost:3000** in your browser
2. Login or continue as guest
3. Select a concession stand
4. Add items to cart
5. Proceed to checkout
6. Use test card: `4242 4242 4242 4242`
7. Complete payment

## 📦 Project Components

### Frontend/ 
**Purpose**: Customer-facing web application

**Key Files**:
- `index.html` - Login/authentication page
- `concessions.html` - Concession selection interface
- `checkout.html` - Payment processing page
- `src/PizzaMenuMVP.jsx` - Pizza menu component
- `src/CoffeeMenuMVP.jsx` - Coffee menu component

**Features**:
- Multi-page application flow
- Responsive design
- Stripe payment integration
- Real-time cart management

**[View Full Frontend Documentation →](Frontend/README.md)**

### seatserve-backend/
**Purpose**: Active REST API backend

**Key Features**:
- FastAPI REST endpoints
- Stripe payment processing
- Order management
- Table management
- SQLite database

**API Endpoints**:
- `GET /api/menu` - Get menu items
- `POST /api/orders` - Create order
- `POST /api/stripe/create-payment-intent` - Create payment
- `POST /api/stripe/webhook` - Handle Stripe events

**[View Full Backend Documentation →](seatserve-backend/README.md)**

### backend/
**Purpose**: Django payment models (future use)

**Contains**:
- `Payment` model - Payment transaction records
- `PaymentLog` model - Payment event audit trail

**Status**: Not currently integrated with active application

**[View Django Models Documentation →](backend/README.md)**

## 📖 Documentation

### Detailed Documentation by Component

| Component | Documentation | Description |
|-----------|--------------|-------------|
| **Frontend** | [Frontend/README.md](Frontend/README.md) | Complete frontend setup, features, and usage |
| **FastAPI Backend** | [seatserve-backend/README.md](seatserve-backend/README.md) | API endpoints, configuration, deployment |
| **Django Models** | [backend/README.md](backend/README.md) | Payment model schemas and examples |
| **Stripe Setup** | [seatserve-backend/STRIPE_SETUP.md](seatserve-backend/STRIPE_SETUP.md) | Stripe integration guide |

### API Documentation

Once the backend is running, access interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testing

### Frontend Testing
```bash
cd Frontend
npm run lint
```

### Backend Testing
```bash
cd seatserve-backend
pytest test_main.py -v
```

### Stripe Test Cards

| Card Number | Scenario |
|------------|----------|
| `4242 4242 4242 4242` | Successful payment |
| `4000 0025 0000 3155` | Requires authentication |
| `4000 0000 0000 9995` | Card declined |

Use any future expiration, any CVV, any ZIP code.

## 🔐 Security

- **Environment Variables** - All secrets stored in `.env` files
- **Never commit** `.env` files to version control
- **HTTPS Ready** - Production ready for SSL/TLS
- **PCI Compliance** - Stripe handles card data
- **Input Validation** - Pydantic models validate all inputs
- **SQL Injection Protection** - Parameterized queries

## 🐛 Troubleshooting

### Backend Won't Start
- Check if port 8000 is in use: `lsof -ti:8000 | xargs kill`
- Verify Python dependencies: `pip install -r requirements.txt`
- Check `.env` file exists with Stripe keys

### Frontend Won't Start
- Check if port 3000 is in use: `lsof -ti:3000 | xargs kill`
- Reinstall dependencies: `rm -rf node_modules && npm install`

### Payment Issues
- Verify Stripe keys in backend `.env`
- Ensure backend is running on port 8000
- Check browser console for errors
- Use Stripe test cards only in development

## 🚧 Future Enhancements

- [ ] Real-time order tracking with WebSockets
- [ ] Push notifications for order updates
- [ ] Admin dashboard for vendors
- [ ] Mobile app (iOS/Android)
- [ ] PostgreSQL for production
- [ ] Redis caching
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Comprehensive test coverage
- [ ] Order history and analytics

## 📄 License

Demo MVP Project - All Rights Reserved © 2025 SeatServe

## 🤝 Contributing

This is a demo project. For questions or collaboration:

- **Héctor Soto** - [@hector17rock](https://github.com/hector17rock)
- **Alejandro Garcia** - [@GerAle30](https://github.com/GerAle30)

## 📞 Support

For issues or questions:
1. Check component-specific README files
2. Review troubleshooting sections
3. Check logs:
   - Frontend: Browser console
   - Backend: `backend.log` or `/tmp/seatserve_backend.log`
4. Contact the development team

## 🙏 Acknowledgments

- **Stripe** - Payment processing platform
- **FastAPI** - Modern Python web framework
- **React** - Frontend UI library
- **Tailwind CSS** - Utility-first CSS framework

---

<div align="center">

**Status:** ✅ **MVP COMPLETED**

Built with ❤️ by Héctor Soto & Alejandro Garcia

⭐ **Star this repo if you find it useful!** ⭐

</div>
