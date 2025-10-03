"""
Main FastAPI application for SeatServe
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from loguru import logger

from app.config import settings
from app.db import init_db, check_db_connection
from app.routers import menu, orders


# Configure logging
logging.basicConfig(level=getattr(logging, settings.log_level))


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events
    """
    # Startup
    logger.info(f"Starting {settings.app_name} v{settings.version}")
    
    # Check database connection
    if check_db_connection():
        logger.info("Database connection successful")
        # Initialize database tables
        try:
            init_db()
            logger.info("Database initialization completed")
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise
    else:
        logger.error("Database connection failed")
        raise Exception("Cannot connect to database")
    
    yield
    
    # Shutdown
    logger.info("Shutting down SeatServe API")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="""
    SeatServe Restaurant Management API
    
    A comprehensive REST API for restaurant table service management including:
    - Menu management
    - Order processing
    - Table management
    - Staff authentication
    """,
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(500)
async def internal_server_error_handler(request, exc):
    """Handle internal server errors"""
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error",
            "status_code": 500
        }
    )


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.version,
        "status": "running",
        "docs_url": "/docs" if settings.debug else "Contact administrator for API documentation"
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        db_status = check_db_connection()
        return {
            "status": "healthy" if db_status else "unhealthy",
            "database": "connected" if db_status else "disconnected",
            "timestamp": "2024-01-01T00:00:00Z",  # In real app, use datetime.utcnow()
            "version": settings.version
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": "2024-01-01T00:00:00Z"
            }
        )


# API version endpoint
@app.get("/api/v1/info")
async def api_info():
    """API information endpoint"""
    return {
        "api_name": settings.app_name,
        "version": settings.version,
        "restaurant": {
            "name": settings.restaurant_name,
            "address": settings.restaurant_address,
            "phone": settings.restaurant_phone
        },
        "endpoints": {
            "health": "/health",
            "menu": "/api/v1/menu",
            "orders": "/api/v1/orders",
            "documentation": "/docs" if settings.debug else None
        }
    }


# Include routers
app.include_router(
    menu.router,
    prefix="/api/v1/menu",
    tags=["Menu Management"]
)

app.include_router(
    orders.router,
    prefix="/api/v1/orders",
    tags=["Order Management"]
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )