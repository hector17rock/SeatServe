<div align="center">
  <img src="public/Images/seatserve-app-icon.png" alt="SeatServe Logo" width="120" height="120">
</div>

# SeatServe Frontend

A modern, responsive web application for stadium and venue food ordering with seat delivery and pickup options. Built with Vite, Tailwind CSS, and integrated with Stripe payment processing.

## Authors

**Héctor Soto**  
Frontend Software Engineer  
GitHub: [@hector17rock](https://github.com/hector17rock)

**Alejandro Garcia**  
Backend Software Engineer  
GitHub: [@GerAle30](https://github.com/GerAle30)

## Overview

SeatServe Frontend is a comprehensive customer-facing application that allows users to browse menus from multiple concessions, place orders, and complete secure payments. The application features a beautiful UI with gradient designs, smooth animations, and an intuitive user experience.

## ✨ Features

### User Experience
- **Multi-Page Application**: Login, concession selection, checkout, order review, and confirmation pages
- **Guest & Authenticated Access**: Users can sign up, log in, or continue as a guest
- **Responsive Design**: Optimized for mobile, tablet, and desktop devices
- **Beautiful UI**: Modern gradient designs with Tailwind CSS
- **Real-time Cart Management**: Live cart updates with localStorage persistence

### Concession System
- **Multiple Vendors**: Browse different concession stands (Pizza, Coffee, Burgers, etc.)
- **Menu Categories**: Organized by food type with filtering options
- **Dynamic Pricing**: Real-time cart calculations with tax

### Payment Integration
- **Stripe Integration**: Secure payment processing with Stripe Elements
- **Card Type Detection**: Automatic detection of Visa, Mastercard, Amex, and Discover
- **Payment Validation**: Real-time card validation and error handling
- **Billing Information**: Comprehensive billing address collection
- **Order Summary**: Clear breakdown of items, subtotal, tax, and total

### Order Management
- **Order Review**: Review order details before final confirmation
- **Order Confirmation**: Beautiful confirmation page with order details
- **Order History**: Track orders via localStorage

## 🛠 Tech Stack

### Core Technologies
- **Vite 5.0.8** - Lightning-fast build tool and dev server
- **React 18.2.0** - UI framework for dynamic components
- **Tailwind CSS 3.3.6** - Utility-first CSS framework

### Development Tools
- **ESLint** - Code linting and quality
- **PostCSS** - CSS processing with Autoprefixer
- **TypeScript types** - Type definitions for React

### Payment Processing
- **Stripe.js v3** - Secure payment processing
- **Stripe Elements** - Pre-built UI components for card input

### State Management
- **localStorage** - Client-side state persistence
- **In-memory state** - For real-time cart updates

## 📁 Project Structure

```
frontend/
├── public/
│   ├── Images/                    # App icons and concession logos
│   │   ├── seatserve-app-icon.png
│   │   ├── index-wallpaper.png
│   │   ├── napoli-pizza-logo.png
│   │   ├── brewline-coffee-logo.png
│   │   └── ...
│   └── favicon.ico
├── src/
│   ├── Auth.jsx                   # Authentication component
│   ├── SeatServeMVP.jsx          # Main menu/ordering component
│   ├── PizzaMenuMVP.jsx          # Pizza concession menu
│   ├── CoffeeMenuMVP.jsx         # Coffee concession menu
│   ├── IceCreamMenuMVP.jsx       # Ice cream menu
│   ├── SnacksMenuMVP.jsx         # Snacks menu
│   ├── main.jsx                   # Entry point
│   ├── index.css                  # Global styles
│   └── menu*.jsx                  # Additional menu components
├── index.html                     # Login page
├── signup.html                    # Registration page
├── concessions.html               # Concession selection page
├── checkout.html                  # Payment page
├── order_review.html              # Order review page
├── confirmation.html              # Order confirmation page
├── signup_confirmation.html       # Sign-up success page
├── menu*.html                     # Various menu pages
├── package.json                   # Dependencies and scripts
├── vite.config.js                 # Vite configuration
├── tailwind.config.js             # Tailwind configuration
├── postcss.config.js              # PostCSS configuration
├── .eslintrc.json                 # ESLint configuration
└── README.md                      # This file
```

## 🚀 Getting Started

### Prerequisites

- **Node.js** (version 16 or higher)
- **npm** or **yarn**
- Backend server running on `http://localhost:8000` (for payment processing)

### Installation

1. **Clone the repository:**
```bash
cd /Users/hector/SeatServe/frontend
```

2. **Install dependencies:**
```bash
npm install
```

### Development

**Start the development server:**
```bash
npm run dev
```

The application will be available at **http://localhost:3000**

### Building for Production

**Build the application:**
```bash
npm run build
```

The optimized files will be in the `dist/` directory.

**Preview production build:**
```bash
npm run preview
```

## 📱 Application Flow

### 1. Login/Authentication (`index.html`)
- Users can sign in with email/password
- Guest access available
- Links to sign-up page

### 2. Sign Up (`signup.html`)
- New user registration
- Form validation
- Account creation with localStorage

### 3. Concession Selection (`concessions.html`)
- Browse available concession stands
- View operating hours and categories
- Select a vendor to view menu

### 4. Menu/Ordering (`menu*.html`)
- Browse menu items by category
- Add items to cart with quantity selection
- View real-time cart total
- Proceed to checkout

### 5. Checkout (`checkout.html`)
- Review order summary
- Enter payment information via Stripe
- Automatic card type detection
- Billing address collection
- Complete secure payment

### 6. Order Review (`order_review.html`)
- Review order details before submission
- Edit or confirm order
- Submit to kitchen

### 7. Confirmation (`confirmation.html`)
- Order confirmation with details
- Order number and estimated time
- Return to concessions option

## 💳 Payment Integration

### Stripe Setup

The application integrates with Stripe for secure payment processing:

1. **Backend Configuration**: Stripe keys are configured in the backend `.env` file
2. **Frontend Integration**: Checkout page loads Stripe.js and creates payment elements
3. **Payment Flow**:
   - Create Payment Intent on backend
   - Collect card details via Stripe Elements
   - Confirm payment with Stripe API
   - Handle success/error responses

### Supported Payment Methods
- Visa
- Mastercard
- American Express
- Discover

### Test Cards

Use these test card numbers in development:
- **Success**: `4242 4242 4242 4242`
- **Requires authentication**: `4000 0025 0000 3155`
- **Declined**: `4000 0000 0000 9995`

Use any future expiration date (e.g., `12/34`), any 3-digit CVV, and any 5-digit ZIP code.

## 🎨 Design Features

### Color Scheme
- **Primary**: Emerald (Green) - `#10b981`
- **Secondary**: Cyan (Blue) - `#06b6d4`
- **Gradients**: Emerald to Cyan for CTAs and branding
- **Neutral**: Gray scale for text and backgrounds

### UI Components
- **Rounded corners**: Consistent use of `rounded-xl` and `rounded-2xl`
- **Shadows**: Subtle elevation with `shadow-sm` and `shadow-2xl`
- **Transitions**: Smooth hover effects on all interactive elements
- **Backdrop blur**: Frosted glass effect on headers
- **Custom SVG icons**: Hand-crafted payment card icons

### Responsive Breakpoints
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

## 🔧 Configuration

### Vite Configuration (`vite.config.js`)

```javascript
{
  server: {
    port: 3000,              // Development server port
    host: '0.0.0.0',         // Allow external connections
    proxy: {
      '/api': {
        target: 'http://localhost:8000',  // Backend API
        changeOrigin: true,
        secure: false
      }
    }
  }
}
```

### Tailwind Configuration (`tailwind.config.js`)

Tailwind is configured via CDN in HTML files for rapid development.

## 📦 Dependencies

### Production Dependencies
- `react@^18.2.0` - UI library
- `react-dom@^18.2.0` - React DOM renderer

### Development Dependencies
- `vite@^5.0.8` - Build tool
- `@vitejs/plugin-react@^4.2.1` - React plugin for Vite
- `tailwindcss@^3.3.6` - CSS framework
- `autoprefixer@^10.4.16` - CSS vendor prefixing
- `postcss@^8.4.32` - CSS processing
- `eslint@^8.55.0` - Code linting
- ESLint React plugins

## 🔐 Security Features

- **No inline secrets**: All API keys stored on backend
- **HTTPS ready**: Production build ready for SSL
- **Input validation**: Client-side validation for all forms
- **XSS protection**: React's built-in XSS protection
- **Secure payment**: PCI-compliant via Stripe

## 🌐 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## 📝 Available Scripts

| Script | Command | Description |
|--------|---------|-------------|
| **dev** | `npm run dev` | Start development server |
| **build** | `npm run build` | Build for production |
| **preview** | `npm run preview` | Preview production build |
| **lint** | `npm run lint` | Run ESLint |

## 🐛 Troubleshooting

### Payment System Issues

**Error: "Unable to load payment system"**
- Ensure backend server is running on `http://localhost:8000`
- Check that Stripe keys are configured in backend `.env` file
- Verify network connectivity to backend

**Card Element Not Showing**
- Check browser console for Stripe.js errors
- Verify Stripe publishable key is valid
- Clear browser cache and reload

### Development Server Issues

**Port 3000 Already in Use**
- Change port in `vite.config.js`
- Or kill process using port 3000: `lsof -ti:3000 | xargs kill`

**Module Not Found Errors**
- Run `npm install` to install dependencies
- Delete `node_modules` and `package-lock.json`, then reinstall

## 🔄 State Management

The application uses localStorage for state persistence:

### Stored Data
- `seatserve_logged_in` - Login status
- `seatserve_user` - User name
- `seatserve_accounts` - Registered accounts
- `selected_concession_id` - Selected vendor
- `selected_concession_name` - Vendor name
- `pending_order` - Current order data
- `latest_order` - Last completed order

### Cart Data Structure
```javascript
{
  items: [
    { id: "123", name: "Pizza", price: 12.99, qty: 2 }
  ],
  total: 25.98,
  concession: "Napoli Pizza",
  timestamp: "2025-01-10T15:30:00Z"
}
```

## 🚧 Future Enhancements

- [ ] Real-time order tracking
- [ ] Push notifications for order updates
- [ ] Saved payment methods
- [ ] Order history dashboard
- [ ] Loyalty rewards program
- [ ] Multiple language support
- [ ] Dark mode toggle
- [ ] Accessibility improvements (WCAG 2.1)

## 📄 License

Demo MVP Project - All Rights Reserved © 2025 SeatServe

## 🤝 Related Projects

- **Backend**: `/Users/hector/SeatServe/seatserve-backend/`
- **Django Models**: `/Users/hector/SeatServe/backend/`

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review backend logs at `/tmp/seatserve_backend.log`
3. Check frontend logs at `/tmp/seatserve_frontend.log`
4. Contact the development team

---

**Status:** ✅ **COMPLETED**

Built with ❤️ by Héctor Soto & Alejandro Garcia
