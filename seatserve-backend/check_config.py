#!/usr/bin/env python3
"""
Configuration verification script for SeatServe API
"""
from app.config import settings
import sys

def main():
    print("SeatServe Configuration Check")
    print("=" * 40)
    
    # Application Settings
    print("\nApplication Settings:")
    print(f"   Name: {settings.app_name}")
    print(f"   Version: {settings.version}")
    print(f"   Debug Mode: {settings.debug}")
    print(f"   Host: {settings.host}")
    print(f"   Port: {settings.port}")
    
    # Database
    print("\nDatabase Settings:")
    print(f"   URL: {settings.database_url}")
    print(f"   Auto-constructed PostgreSQL URL: {settings.postgres_url}")
    print(f"   Active Database URL: {settings.get_database_url()}")
    
    # Security
    print("\nSecurity Settings:")
    print(f"   Secret Key: {'***' if settings.secret_key != 'your-secret-key-here-change-in-production-please' else 'DEFAULT KEY (CHANGE THIS!)'}")
    print(f"   Algorithm: {settings.algorithm}")
    print(f"   Token Expiry: {settings.access_token_expire_minutes} minutes")
    
    # CORS
    print("\nCORS Settings:")
    print(f"   Allowed Origins: {settings.cors_origins}")
    
    # Restaurant Info
    print("\nRestaurant Information:")
    print(f"   Name: {settings.restaurant_name}")
    print(f"   Address: {settings.restaurant_address}")
    print(f"   Phone: {settings.restaurant_phone}")
    print(f"   Email: {settings.restaurant_email}")
    
    # Business Logic
    print("\nBusiness Settings:")
    print(f"   Tax Rate: {settings.default_tax_rate * 100}%")
    print(f"   Service Charge: {settings.default_service_charge * 100}%")
    print(f"   Currency: {settings.currency}")
    print(f"   Timezone: {settings.timezone}")
    
    # Optional Services
    print("\nOptional Services:")
    print(f"   Redis Enabled: {settings.redis_enabled}")
    print(f"   Redis URL: {settings.redis_url}")
    print(f"   SMTP Host: {settings.smtp_host or '(not configured)'}")
    
    # Development Settings
    print("\nDevelopment Settings:")
    print(f"   Swagger Docs: {settings.enable_swagger}")
    print(f"   ReDoc: {settings.enable_redoc}")
    print(f"   Log Level: {settings.log_level}")
    
    # File Upload
    print("\nFile Upload Settings:")
    print(f"   Max File Size: {settings.max_file_size / (1024*1024):.1f} MB")
    print(f"   Upload Path: {settings.upload_path}")
    
    # Environment Detection
    print("\nEnvironment Detection:")
    print(f"   Is Development: {settings.is_development()}")
    print(f"   Is Production: {settings.is_production()}")
    
    # Security Warnings
    print("\nSecurity Check:")
    warnings = []
    
    if settings.secret_key == "your-secret-key-here-change-in-production-please":
        warnings.append("Using default secret key - CHANGE THIS!")
    
    if settings.debug and settings.is_production():
        warnings.append("Debug mode enabled in production!")
    
    if not warnings:
        print("   No security issues found")
    else:
        print("   Security Issues:")
        for warning in warnings:
            print(f"      • {warning}")
    
    print("\n" + "=" * 40)
    print("Configuration check completed!")
    
    if warnings:
        print("Please address security warnings before deploying to production")
        return 1
    else:
        print("Configuration looks good!")
        return 0

if __name__ == "__main__":
    sys.exit(main())