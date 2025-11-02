#!/bin/bash

# 🍽️ SeatServe - Installation Script for Dependencies
# This script installs all dependencies for both Frontend and Backend

set -e  # Exit on any error

echo "🍽️ SeatServe - Installing Dependencies"
echo "======================================"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -d "Frontend" ] || [ ! -d "seatserve-backend" ]; then
    print_error "Este script debe ejecutarse desde el directorio raíz de SeatServe"
    exit 1
fi

echo ""
print_status "🔧 Installing Backend Dependencies (Python/FastAPI)..."
echo "------------------------------------------------------"

# Navigate to backend directory
cd seatserve-backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
print_status "Activating virtual environment and installing Python packages..."
source venv/bin/activate

# Upgrade pip first
pip install --upgrade pip

# Install backend dependencies
if [ -f "requirements.txt" ]; then
    print_status "Installing from requirements.txt..."
    pip install -r requirements.txt
    print_success "Backend dependencies installed successfully!"
else
    print_error "requirements.txt not found in seatserve-backend directory"
    exit 1
fi

# Deactivate virtual environment
deactivate

# Go back to root directory
cd ..

echo ""
print_status "🌐 Installing Frontend Dependencies (Node.js/React)..."
echo "-----------------------------------------------------"

# Navigate to frontend directory
cd Frontend

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    print_error "Node.js no está instalado. Por favor instala Node.js primero:"
    print_error "curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -"
    print_error "sudo apt-get install -y nodejs"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    print_error "npm no está instalado. Por favor instala npm primero."
    exit 1
fi

print_status "Node.js version: $(node --version)"
print_status "npm version: $(npm --version)"

# Install frontend dependencies
if [ -f "package.json" ]; then
    print_status "Installing Node.js packages..."
    npm install
    print_success "Frontend dependencies installed successfully!"
else
    print_error "package.json not found in Frontend directory"
    exit 1
fi

# Go back to root directory
cd ..

echo ""
print_success "🎉 All dependencies installed successfully!"
echo "========================================"
echo ""
echo "📋 Next steps:"
echo "---------------"
echo "1. Backend (FastAPI):"
echo "   cd seatserve-backend"
echo "   source venv/bin/activate"
echo "   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "2. Frontend (React/Vite):"
echo "   cd Frontend"
echo "   npm run dev"
echo ""
echo "3. Access your application:"
echo "   - Frontend: http://localhost:5173"
echo "   - Backend API: http://localhost:8000"
echo "   - API Documentation: http://localhost:8000/docs"
echo ""
print_success "¡SeatServe está listo para usar! 🚀"