"""
Configuration settings for SeatServe API
"""
from pydantic_settings import BaseSettings
from pydantic import ConfigDict, Field
from typing import List, Union, Optional
import os


class Settings(BaseSettings):
    """Application settings with comprehensive configuration options"""
    
    # Application Settings
    app_name: str = Field(default="SeatServe API", description="Application name")
    version: str = Field(default="1.0.0", description="Application version")
    debug: bool = Field(default=True, description="Debug mode")
    host: str = Field(default="0.0.0.0", description="Host to bind to")
    port: int = Field(default=8000, description="Port to bind to")
    
    # Database Configuration
    database_url: str = Field(
        default="sqlite:///./seatserve.db",
        description="Database connection URL"
    )
    
    # Alternative database settings for PostgreSQL
    db_host: str = Field(default="localhost", description="Database host")
    db_port: int = Field(default=5432, description="Database port")
    db_name: str = Field(default="seatserve_db", description="Database name")
    db_user: str = Field(default="seatserve_user", description="Database user")
    db_password: str = Field(default="seatserve_password", description="Database password")
    
    # Security Configuration
    secret_key: str = Field(
        default="your-secret-key-here-change-in-production-please",
        description="JWT secret key"
    )
    algorithm: str = Field(default="HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(
        default=120, 
        description="Access token expiration time in minutes"
    )
    
    # Additional API Keys (for future features)
    concession_api_key: str = Field(
        default="concession-dev-key", 
        description="API key for concession operations"
    )
    runner_api_key: str = Field(
        default="runner-dev-key", 
        description="API key for runner operations"
    )
    
    # CORS Configuration
    allowed_origins: Union[str, List[str]] = Field(
        default="http://localhost:3000,http://127.0.0.1:3000,http://localhost:8080",
        description="Allowed CORS origins"
    )
    
    # Restaurant Information
    restaurant_name: str = Field(
        default="SeatServe Restaurant", 
        description="Restaurant name"
    )
    restaurant_address: str = Field(
        default="123 Main Street, City, State 12345", 
        description="Restaurant address"
    )
    restaurant_phone: str = Field(
        default="+1-234-567-8900", 
        description="Restaurant phone"
    )
    restaurant_email: str = Field(
        default="info@seatserve.com", 
        description="Restaurant email"
    )
    
    # Email Configuration (Optional)
    smtp_host: str = Field(default="", description="SMTP host for email")
    smtp_port: int = Field(default=587, description="SMTP port")
    smtp_username: str = Field(default="", description="SMTP username")
    smtp_password: str = Field(default="", description="SMTP password")
    smtp_use_tls: bool = Field(default=True, description="Use TLS for SMTP")
    
    # Redis Configuration (Optional - for caching/sessions)
    redis_url: str = Field(
        default="redis://localhost:6379/0", 
        description="Redis connection URL"
    )
    redis_enabled: bool = Field(default=False, description="Enable Redis")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format"
    )
    
    # File Upload Configuration
    max_file_size: int = Field(
        default=10 * 1024 * 1024,  # 10MB
        description="Maximum file upload size in bytes"
    )
    upload_path: str = Field(
        default="./uploads", 
        description="Path for uploaded files"
    )
    
    # Business Logic Configuration
    default_tax_rate: float = Field(
        default=0.08, 
        description="Default tax rate for orders"
    )
    default_service_charge: float = Field(
        default=0.15, 
        description="Default service charge"
    )
    currency: str = Field(default="USD", description="Default currency")
    timezone: str = Field(default="UTC", description="Default timezone")
    
    # Development/Testing flags
    enable_swagger: bool = Field(default=True, description="Enable Swagger docs")
    enable_redoc: bool = Field(default=True, description="Enable ReDoc")
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    @property
    def cors_origins(self) -> List[str]:
        """Parse CORS origins from string or return list"""
        if isinstance(self.allowed_origins, str):
            return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]
        return self.allowed_origins
    
    @property
    def postgres_url(self) -> str:
        """Generate PostgreSQL URL from individual components"""
        return f"postgresql+psycopg2://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    def get_database_url(self) -> str:
        """Get the appropriate database URL"""
        if self.database_url.startswith(("sqlite", "postgresql", "mysql")):
            return self.database_url
        else:
            # If database_url is not a proper URL, construct PostgreSQL URL
            return self.postgres_url
    
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.debug
    
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return not self.debug


# Create global settings instance
settings = Settings()
