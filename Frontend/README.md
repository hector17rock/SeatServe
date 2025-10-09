# SeatServe Frontend MVP

A React-based frontend application for stadium food ordering with seat delivery and pickup options.

## Features

- **Two interfaces:**
  - **Fan View**: Browse menu, add items to cart, place orders
  - **Concession View**: Manage incoming orders, advance order status

- **Ordering options:**
  - Pickup at counter
  - Seat delivery with location input

- **Menu filtering:**
  - Search by item name
  - Filter by category (Food, Snacks, Drinks, Dessert)
  - Filter by preparation station

- **Order management:**
  - Real-time status updates (Queued → Preparing → Ready → Delivered)
  - Order notes support
  - Cancel orders functionality

## Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling
- **In-memory state management** - No backend required

## Getting Started

### Prerequisites

- Node.js (version 16 or higher)
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

### Development

1. Start the development server:
```bash
npm run dev
```

2. Open your browser to `http://localhost:3000`

### Building for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

### Preview Production Build

```bash
npm run preview
```

## Usage

### Login

1. Open `http://localhost:3000` to access the login page
2. You can either:
   - Enter any email/password and click "Sign In" (demo login)
   - Click "Continue as Guest" for immediate access
3. You'll be redirected to the menu page

### As a Fan (Customer)

1. Switch to the "Fan" tab
2. Browse the menu using search and filters
3. Add items to your cart using the "Add" button
4. Adjust quantities with + and - buttons
5. Choose fulfillment method (Pickup or Seat Delivery)
6. If choosing seat delivery, enter your seat location
7. Add any special notes
8. Click "Place Order" to submit

### As Concession Staff

1. Switch to the "Concession" tab
2. View all incoming orders with status indicators
3. Use "Advance" button to move orders through status flow:
   - Queued → Preparing → Ready → Delivered
4. Use "Cancel" button to remove orders if needed

## Project Structure

```
Frontend/
├── src/
│   ├── SeatServeMVP.jsx    # Main React component
│   ├── main.jsx            # Entry point
│   └── index.css           # Tailwind CSS imports
├── index.html              # Login page
├── menu1.html              # React app (menu/ordering)
├── package.json            # Dependencies and scripts
├── vite.config.js          # Vite configuration
├── tailwind.config.js      # Tailwind configuration
└── postcss.config.js       # PostCSS configuration
```

## Development Notes

- This is a frontend-only MVP with in-memory state
- No backend or database required
- Orders are lost on page refresh
- Includes built-in smoke tests that run in development mode
- Responsive design optimized for mobile and desktop

## Menu Items

The application includes these sample menu items:
- **Food**: Classic Burger, Cheese Pizza Slice, Chicken Tenders, Nachos Supreme
- **Snacks**: Popcorn, Soft Pretzel
- **Drinks**: Soda (Large), Bottled Water, Coffee
- **Dessert**: Ice Cream Cup

## Customization

To customize the menu items, edit the `CATALOG` array in `src/SeatServeMVP.jsx`:

```javascript
const CATALOG = [
  { id: "p1", name: "Custom Item", price: 12.0, category: "Food", station: "Grill" },
  // Add more items...
];
```

## Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## License

This is a demo MVP project.