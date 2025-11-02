#!/usr/bin/env python3
"""
SeatServe Backend - Main Application Entry Point
Restaurant table service management system
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import json
from datetime import datetime
import uvicorn
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="SeatServe API",
    version="1.0.0",
    description="""
    🍽️ SeatServe Restaurant Management API
    
    A comprehensive REST API for restaurant table service management including:
    - Menu management
    - Order processing
    - Table management
    - Real-time updates
    """,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Middleware para logging de todas las peticiones

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log de petición entrante
        logger.info(f"📨 [{request.method}] {request.url.path}")
        
        # Capturar body si existe
        if request.method in ["POST", "PUT"]:
            try:
                body = await request.body()
                if body:
                    logger.info(f"📦 Body recibido: {body.decode()}")
                # Recrear el stream para que FastAPI lo pueda leer
                async def receive():
                    return {"type": "http.request", "body": body}
                request._receive = receive
            except Exception as e:
                logger.error(f"Error leyendo body: {e}")
        
        response = await call_next(request)
        logger.info(f"✅ Respuesta enviada: {response.status_code}")
        return response

app.add_middleware(LoggingMiddleware)

# Pydantic models
class MenuItem(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    price: float
    category: str
    available: bool = True

class Order(BaseModel):
    id: Optional[int] = None
    table_number: int
    items: List[dict]
    total: float
    status: str = "pending"
    timestamp: Optional[str] = None

class Table(BaseModel):
    id: Optional[int] = None
    number: int
    seats: int
    status: str = "available"  # available, occupied, reserved

# Database initialization
def init_db():
    """Initialize SQLite database with sample data"""
    conn = sqlite3.connect('seatserve.db')
    cursor = conn.cursor()
    
    # Create menu table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            category TEXT NOT NULL,
            available BOOLEAN DEFAULT 1
        )
    ''')
    
    # Create orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_number INTEGER NOT NULL,
            items TEXT NOT NULL,
            total REAL NOT NULL,
            status TEXT DEFAULT 'pending',
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create tables table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS restaurant_tables (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number INTEGER UNIQUE NOT NULL,
            seats INTEGER NOT NULL,
            status TEXT DEFAULT 'available'
        )
    ''')
    
    # Insert sample menu items if table is empty
    cursor.execute('SELECT COUNT(*) FROM menu_items')
    if cursor.fetchone()[0] == 0:
        sample_menu = [
            ("Margherita Pizza", "Fresh tomato, mozzarella, basil", 12.99, "Mains"),
            ("Caesar Salad", "Romaine lettuce, parmesan, croutons", 8.99, "Salads"),
            ("Grilled Salmon", "Atlantic salmon with vegetables", 18.99, "Mains"),
            ("Chocolate Cake", "Rich chocolate cake with vanilla ice cream", 6.99, "Desserts"),
            ("Coffee", "Freshly brewed coffee", 2.99, "Beverages"),
            ("Burger Classic", "Beef patty with cheese and fries", 14.99, "Mains"),
            ("Greek Salad", "Fresh vegetables with feta cheese", 9.99, "Salads"),
            ("Tiramisu", "Traditional Italian dessert", 7.99, "Desserts")
        ]
        
        cursor.executemany(
            'INSERT INTO menu_items (name, description, price, category) VALUES (?, ?, ?, ?)',
            sample_menu
        )
    
    # Insert sample tables if table is empty
    cursor.execute('SELECT COUNT(*) FROM restaurant_tables')
    if cursor.fetchone()[0] == 0:
        sample_tables = [
            (1, 4), (2, 2), (3, 6), (4, 4), (5, 8), (6, 2), (7, 4), (8, 6)
        ]
        cursor.executemany(
            'INSERT INTO restaurant_tables (number, seats) VALUES (?, ?)',
            sample_tables
        )
    
    conn.commit()
    conn.close()

# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def root():
    """Welcome page with API information"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SeatServe API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .header { text-align: center; color: #333; border-bottom: 2px solid #e74c3c; padding-bottom: 20px; margin-bottom: 30px; }
            .endpoint { background: #ecf0f1; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .method { font-weight: bold; color: #e74c3c; }
            .description { color: #666; margin-top: 5px; }
            .footer { text-align: center; margin-top: 30px; color: #666; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🍽️ SeatServe API</h1>
                <p>Restaurant Table Service Management System</p>
            </div>
            
            <h2>📋 Available Endpoints</h2>
            
            <div class="endpoint">
                <div class="method">GET /docs</div>
                <div class="description">Interactive Swagger API Documentation</div>
            </div>
            
            <div class="endpoint">
                <div class="method">GET /health</div>
                <div class="description">API Health Check</div>
            </div>
            
            <div class="endpoint">
                <div class="method">GET /api/menu</div>
                <div class="description">Get all menu items</div>
            </div>
            
            <div class="endpoint">
                <div class="method">POST /api/menu</div>
                <div class="description">Create a new menu item</div>
            </div>
            
            <div class="endpoint">
                <div class="method">GET /api/orders</div>
                <div class="description">Get all orders</div>
            </div>
            
            <div class="endpoint">
                <div class="method">POST /api/orders</div>
                <div class="description">Create a new order</div>
            </div>
            
            <div class="endpoint">
                <div class="method">GET /api/tables</div>
                <div class="description">Get all restaurant tables</div>
            </div>
            
            <div class="footer">
                <p>🚀 <strong>Status:</strong> Running | <strong>Version:</strong> 1.0.0</p>
                <p>Visit <a href="/docs">/docs</a> for interactive API documentation</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "SeatServe API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

# Menu endpoints
@app.get("/api/menu", response_model=List[MenuItem])
async def get_menu():
    """Get all menu items"""
    logger.info("📋 Obteniendo menú")
    try:
        conn = sqlite3.connect('seatserve.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM menu_items WHERE available = 1')
        items = cursor.fetchall()
        conn.close()
        
        menu_items = []
        for item in items:
            menu_items.append(MenuItem(
                id=item[0],
                name=item[1],
                description=item[2],
                price=item[3],
                category=item[4],
                available=bool(item[5])
            ))
        
        logger.info(f"✅ Menú obtenido: {len(menu_items)} items encontrados")
        return menu_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching menu: {str(e)}")

@app.get("/api/menu/categories")
async def get_menu_categories():
    """Get all menu categories"""
    try:
        conn = sqlite3.connect('seatserve.db')
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT category FROM menu_items')
        categories = [row[0] for row in cursor.fetchall()]
        conn.close()
        return {"categories": categories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching categories: {str(e)}")

@app.post("/api/menu", response_model=MenuItem)
async def create_menu_item(item: MenuItem):
    """Create a new menu item"""
    logger.info(f"🍽️ Nuevo item de menú recibido: {item.name} - ${item.price}")
    logger.debug(f"Datos completos: {item.dict()}")
    try:
        conn = sqlite3.connect('seatserve.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO menu_items (name, description, price, category, available)
            VALUES (?, ?, ?, ?, ?)
        ''', (item.name, item.description, item.price, item.category, item.available))
        
        item_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        item.id = item_id
        logger.info(f"✅ Item de menú creado con ID: {item_id}")
        return item
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating menu item: {str(e)}")

# Order endpoints
@app.get("/api/orders", response_model=List[Order])
async def get_orders():
    """Get all orders"""
    logger.info("📦 Obteniendo ordenes")
    try:
        conn = sqlite3.connect('seatserve.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM orders ORDER BY timestamp DESC')
        orders_data = cursor.fetchall()
        conn.close()
        
        orders = []
        for order_data in orders_data:
            orders.append(Order(
                id=order_data[0],
                table_number=order_data[1],
                items=json.loads(order_data[2]),
                total=order_data[3],
                status=order_data[4],
                timestamp=order_data[5]
            ))
        
        logger.info(f"✅ Ordenes obtenidas: {len(orders)} ordenes encontradas")
        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching orders: {str(e)}")

@app.post("/api/orders", response_model=Order)
async def create_order(order: Order):
    """Create a new order"""
    logger.info(f"🛎️ Nueva orden recibida - Mesa: {order.table_number}, Total: ${order.total}")
    logger.info(f"📋 Items en la orden: {order.items}")
    logger.debug(f"Datos completos de la orden: {order.dict()}")
    try:
        conn = sqlite3.connect('seatserve.db')
        cursor = conn.cursor()
        
        items_json = json.dumps(order.items)
        timestamp = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT INTO orders (table_number, items, total, status, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (order.table_number, items_json, order.total, order.status, timestamp))
        
        order_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        order.id = order_id
        order.timestamp = timestamp
        logger.info(f"✅ Orden creada con ID: {order_id} a las {timestamp}")
        return order
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating order: {str(e)}")

# Table endpoints
@app.get("/api/tables", response_model=List[Table])
async def get_tables():
    """Get all restaurant tables"""
    logger.info("🪑 Obteniendo mesas del restaurante")
    try:
        conn = sqlite3.connect('seatserve.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM restaurant_tables ORDER BY number')
        tables_data = cursor.fetchall()
        conn.close()
        
        tables = []
        for table_data in tables_data:
            tables.append(Table(
                id=table_data[0],
                number=table_data[1],
                seats=table_data[2],
                status=table_data[3]
            ))
        
        logger.info(f"✅ Mesas obtenidas: {len(tables)} mesas encontradas")
        return tables
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching tables: {str(e)}")

@app.put("/api/tables/{table_id}/status")
async def update_table_status(table_id: int, status: str):
    """Update table status"""
    valid_statuses = ["available", "occupied", "reserved"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Status must be one of: {valid_statuses}")
    
    logger.info(f"🔄 Actualizando estado de mesa {table_id} a '{status}'")
    
    try:
        conn = sqlite3.connect('seatserve.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE restaurant_tables SET status = ? WHERE id = ?', (status, table_id))
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Table not found")
        
        conn.commit()
        conn.close()
        
        logger.info(f"✅ Estado de mesa {table_id} actualizado a '{status}'")
        return {"message": f"Table {table_id} status updated to {status}"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error actualizando mesa {table_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating table status: {str(e)}")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)