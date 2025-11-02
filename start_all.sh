#!/bin/bash

echo " Iniciando SeatServe (Backend + Frontend)..."
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para cleanup
cleanup() {
    echo ""
    echo -e "${RED}Deteniendo servidores...${NC}"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

trap cleanup SIGINT SIGTERM

# Iniciar Backend
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}▶ Iniciando BACKEND en http://localhost:8000${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

cd /home/alejandro/SeatServe/seatserve-backend
source venv/bin/activate
python3 main.py &
BACKEND_PID=$!

sleep 3

# Iniciar Frontend
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}▶ Iniciando FRONTEND en http://localhost:5173${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

cd /home/alejandro/SeatServe/Frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo -e "${GREEN}✅ Ambos servidores están activos:${NC}"
echo -e "   📱 Frontend:  http://localhost:5173"
echo -e "   🔧 Backend:   http://localhost:8000"
echo -e "   📚 API Docs:  http://localhost:8000/docs"
echo ""
echo -e "${YELLOW}⏸️  Presiona Ctrl+C para detener ambos servidores${NC}"
echo ""

# Mantener los procesos activos
wait
