"""
Pytest configuration for Django Payment model tests

This file sets up Django ORM for testing, configures database, and provides fixtures.
"""

import os
import sys
import django
from django.conf import settings
from unittest.mock import MagicMock, patch

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure Django settings if not already configured
if not settings.configured:
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',  # Use in-memory database for tests
            }
        },
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'app',
        ],
        SECRET_KEY='test-secret-key-for-pytest',
        USE_TZ=True,
    )

# Setup Django
django.setup()

# Now create the tables
from django.core.management import call_command

def pytest_configure(config):
    """Hook that runs before test collection"""
    # Create the database tables for Payment and PaymentLog models
    from django.core.management.sql import emit_post_migrate_signal
    
    try:
        call_command('migrate', '--run-syncdb', verbosity=0)
        emit_post_migrate_signal(2, False, 'default')
    except Exception as e:
        print(f"Migration warning (may be expected): {e}")


import pytest

@pytest.fixture
def mock_order():
    """Fixture providing a mock Order instance"""
    return MockOrder(id=1)


@pytest.fixture
def payment_data(mock_order):
    """Fixture providing common payment creation data"""
    from decimal import Decimal
    
    return {
        'order': mock_order,
        'stripe_payment_intent_id': 'pi_test_fixture_123',
        'amount': Decimal('100.00'),
        'currency': 'USD',
        'payment_method': 'card',
        'status': 'pending',
    }


@pytest.fixture
def payment_log_data():
    """Fixture providing common payment log creation data"""
    return {
        'event_type': 'intent_created',
        'data': {
            'event_id': 'evt_test_123',
            'created': 1234567890,
            'type': 'payment_intent.created',
        },
    }
