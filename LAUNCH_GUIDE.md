# SeatServe - Guía de Uso Rápida

## 🚀 Aplicación En Vivo

La aplicación SeatServe está actualmente corriendo en tu máquina local.

### Acceso Rápido

**Frontend (Interfaz de Usuario):**
```
http://localhost:3000
```

**Backend API (Documentación Interactiva):**
```
http://localhost:8000/docs
```

**Health Check (Estado del Servidor):**
```
http://localhost:8000/health
```

---

## 📱 Cómo Usar la Aplicación

### 1. Interfaz Principal

Cuando abras http://localhost:3000, verás:

- **Encabezado:** Logo de SeatServe con opciones de navegación
- **Panel de Filtros (izquierda):** Busca items, filtra por categoría y estación
- **Catálogo (centro):** Todos los items disponibles para ordenar
- **Carrito (derecha/abajo):** Resumen de tu orden actual

### 2. Seleccionar Items

1. Busca items usando la barra de búsqueda
2. Filtra por categoría (Food, Drinks, Desserts, etc.)
3. Filtra por estación de cocina (Grill, Fry, Beverage, etc.)
4. Haz clic en **"Add"** para agregar items al carrito

### 3. Gestionar tu Carrito

- **Aumentar cantidad:** Haz clic en el botón **"+"** 
- **Disminuir cantidad:** Haz clic en el botón **"-"**
- **Ver detalles:** El carrito muestra el total en tiempo real

### 4. Opciones de Entrega

Elige cómo quieres recibir tu orden:

- **Pickup:** Recoger en la barra de atención
- **Seat Delivery:** Entregar en tu asiento (requiere número de asiento)

Si seleccionas "Seat Delivery", ingresa tu ubicación:
```
Ejemplo: Section 104, Row F, Seat 12
```

### 5. Agregar Notas

En la sección de notas, puedes especificar:
- Preferencias dietéticas
- Instrucciones especiales
- Alergias

Ejemplo: "Sin cebolla, extra queso, picante"

### 6. Confirmar Orden

1. Verifica que todo sea correcto
2. Haz clic en **"Place Order"**
3. Se te redirigirá a la página de confirmación

### 7. Rastrear tu Orden

Después de confirmar:

1. Haz clic en la pestaña **"Order Status"** en el encabezado
2. Verás tu orden con estado actual:
   - **Queued:** Esperando procesamiento
   - **Preparing:** Siendo preparada
   - **Ready:** Lista para recoger
   - **Delivered:** Completada

---

## 🔌 API Endpoints Disponibles

### Menú

```bash
# Obtener todos los items
GET /api/menu

# Obtener categorías
GET /api/menu/categories

# Crear nuevo item (admin)
POST /api/menu
{
  "name": "Burger Especial",
  "description": "Con ingredientes premium",
  "price": 15.99,
  "category": "Mains",
  "available": true
}
```

### Órdenes

```bash
# Ver todas las órdenes
GET /api/orders

# Crear nueva orden
POST /api/orders
{
  "table_number": 1,
  "items": [
    {"id": "p1", "name": "Burger", "qty": 2, "price": 10.0}
  ],
  "total": 20.0,
  "status": "pending"
}
```

### Mesas

```bash
# Ver todas las mesas
GET /api/tables

# Actualizar estado de mesa
PUT /api/tables/{id}/status?status=occupied
# Estados válidos: available, occupied, reserved
```

### Salud del Sistema

```bash
# Verificar estado del servidor
GET /health
```

---

## 🛠️ Características Técnicas

### Backend (FastAPI + Python)

- Framework: FastAPI
- Base de datos: SQLite
- Puerto: 8000
- Hot reload: Habilitado
- CORS: Habilitado para desarrollo

### Frontend (React + Vite)

- Framework: React 18
- Build tool: Vite
- Styling: Tailwind CSS
- Puerto: 3000
- Hot reload: Habilitado

### Base de Datos

- Tipo: SQLite
- Ubicación: `/seatserve-backend/seatserve.db`
- Datos iniciales: 8 items de menú + 8 mesas

---

## 📊 Datos de Ejemplo

### Items del Menú

| Nombre | Precio | Categoría | Estación |
|--------|--------|-----------|----------|
| Classic Burger | $10.00 | Food | Grill |
| Cheese Burger | $11.00 | Food | Grill |
| Chicken Tenders | $9.00 | Food | Fry |
| Soda Small | $2.50 | Drinks | Beverage |
| Soda Medium | $3.00 | Drinks | Beverage |
| Soda Large | $3.50 | Drinks | Beverage |
| Bottled Water | $2.50 | Drinks | Beverage |
| Milkshake | $5.00 | Drinks | Dessert |

### Mesas Disponibles

- Total: 8 mesas
- Capacidades: 2-8 personas
- Estados: available, occupied, reserved

---

## ⚙️ Comandos Útiles

### Detener la Aplicación

```bash
# En la terminal donde está corriendo:
Ctrl + C
```

### Ver Logs

```bash
# Backend logs (uvicorn)
# Se muestran en la terminal del backend

# Frontend logs (Vite)
# Se muestran en la terminal del frontend
```

### Reiniciar Servicios

```bash
# Backend
cd /home/alejandro/SeatServe/seatserve-backend
python3 main.py

# Frontend
cd /home/alejandro/SeatServe/Frontend
npm run dev
```

---

## 🐛 Troubleshooting

### El frontend no carga

1. Verifica que Node.js esté instalado: `node --version`
2. Verifica que npm esté instalado: `npm --version`
3. Reinstala dependencias: `npm install`
4. Limpia caché: `rm -rf node_modules && npm install`

### El backend no responde

1. Verifica que Python 3.10+ esté instalado: `python3 --version`
2. Verifica dependencias: `pip install -r requirements.txt`
3. Verifica puerto 8000 disponible: `lsof -i :8000`

### Puerto 3000 o 8000 en uso

```bash
# Encontrar proceso usando puerto
lsof -i :3000  # Frontend
lsof -i :8000  # Backend

# Matar proceso (reemplaza PID)
kill -9 <PID>
```

### Base de datos corrupta

```bash
# Respaldar BD actual
cp /home/alejandro/SeatServe/seatserve-backend/seatserve.db seatserve.db.bak

# Eliminar BD para que se cree de nuevo
rm /home/alejandro/SeatServe/seatserve-backend/seatserve.db

# Reiniciar backend para recrear BD
```

---

## 📝 Notas Importantes

1. **Desarrollo Local:** Esta aplicación está configurada para desarrollo local
2. **Datos Temporales:** Las órdenes se almacenan en memoria durante la sesión
3. **CORS:** Está habilitado para desarrollo; en producción configurar específicamente
4. **Hot Reload:** Los cambios se reflejan automáticamente sin reiniciar
5. **Base de Datos:** SQLite es adecuada para desarrollo; usar PostgreSQL en producción

---

## 📞 Soporte Rápido

Para más información:

- **Documentación API:** http://localhost:8000/docs
- **ReDoc (API Docs Alternativo):** http://localhost:8000/redoc
- **Backend Health:** http://localhost:8000/health
- **Frontend Console:** Abre DevTools en el navegador (F12)

---

## ✅ Verificación Rápida

Para asegurar que todo funciona:

```bash
# 1. Backend respondiendo
curl http://localhost:8000/health

# 2. Menu disponible
curl http://localhost:8000/api/menu

# 3. Mesas disponibles
curl http://localhost:8000/api/tables

# 4. Frontend corriendo
curl http://localhost:3000
```

---

**¡La aplicación está lista para usar! Disfruta de SeatServe 🎉**

*Última actualización: October 24, 2025*
