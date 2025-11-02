#!/bin/bash

echo "🔍 Verificando conexión entre Backend y Frontend..."
echo ""

# Test 1: Health Check
echo "1️⃣  Probando Health Check..."
HEALTH=$(curl -s http://localhost:8000/health)
if [ ! -z "$HEALTH" ]; then
    echo "✅ Backend respondiendo: $HEALTH"
else
    echo "❌ Backend NO responde en http://localhost:8000"
    exit 1
fi

echo ""

# Test 2: GET Menu
echo "2️⃣  Obteniendo menú..."
MENU=$(curl -s http://localhost:8000/api/menu)
if [ ! -z "$MENU" ]; then
    echo "✅ Menú obtenido:"
    echo "$MENU" | python3 -m json.tool | head -20
else
    echo "❌ Error obteniendo menú"
fi

echo ""

# Test 3: GET Tablas
echo "3️⃣  Obteniendo mesas..."
TABLES=$(curl -s http://localhost:8000/api/tables)
if [ ! -z "$TABLES" ]; then
    echo "✅ Mesas obtenidas:"
    echo "$TABLES" | python3 -m json.tool | head -20
else
    echo "❌ Error obteniendo mesas"
fi

echo ""

# Test 4: POST Orden
echo "4️⃣  Creando orden de prueba..."
ORDER=$(curl -s -X POST http://localhost:8000/api/orders \
  -H "Content-Type: application/json" \
  -d '{"table_number": 5, "items": [{"name": "Test Burger", "qty": 2, "price": 12.99}], "total": 25.98, "status": "pending"}')

if [ ! -z "$ORDER" ]; then
    echo "✅ Orden creada:"
    echo "$ORDER" | python3 -m json.tool
else
    echo "❌ Error creando orden"
fi

echo ""
echo "✨ Pruebas completadas. Verifica los logs en la terminal del backend."
