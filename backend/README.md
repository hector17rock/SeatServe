<div align="center">
  <img src="../Frontend/public/Images/seatserve-app-icon.png" alt="SeatServe Logo" width="120" height="120">
</div>

# SeatServe Backend (Django Models)

This directory contains Django model definitions for the SeatServe payment system. This is a **separate** backend from the main FastAPI application.

## Authors

**Héctor Soto**  
Frontend Software Engineer  
GitHub: [@hector17rock](https://github.com/hector17rock)

**Alejandro Garcia**  
Backend Software Engineer  
GitHub: [@GerAle30](https://github.com/GerAle30)

## Directory Structure

```
backend/
├── app/
│   └── models/
│       └── payment.py          # Django Payment models
└── README.md                   # This file
```

## Overview

This directory contains Django-based data models that define the payment and transaction structure. These models are designed for future integration with a Django-based backend if needed.

### Models Defined

#### `Payment` Model
Stores Stripe payment transaction history with the following features:

**Payment Status Options:**
- `pending` - Payment initiated but not complete
- `succeeded` - Payment successfully completed
- `failed` - Payment failed
- `canceled` - Payment canceled by user or system
- `refunded` - Payment was refunded

**Payment Method Options:**
- `card` - Credit/Debit Card
- `paypal` - PayPal
- `apple_pay` - Apple Pay
- `google_pay` - Google Pay

**Key Fields:**
- Order linkage (one-to-one with Order)
- User information
- Stripe identifiers (payment intent ID, charge ID, customer ID)
- Payment details (amount, currency, method, status)
- Card information (last 4 digits, brand, expiration)
- Receipt information
- Refund tracking
- Timestamps

**Methods:**
- `is_paid()` - Check if payment was successful
- `can_refund()` - Check if payment can be refunded

#### `PaymentLog` Model
Detailed audit log for payment events including:

**Event Types:**
- `intent_created` - Payment Intent Created
- `intent_succeeded` - Payment Intent Succeeded
- `intent_failed` - Payment Intent Failed
- `charge_created` - Charge Created
- `refund_created` - Refund Created
- `webhook_received` - Webhook Received
- `error` - Error occurred

**Features:**
- Links to Payment model
- Stores complete Stripe responses as JSON
- Error message tracking
- Automatic timestamping

## Relationship to Main Backend

The **active backend** for SeatServe is located at:
```
/Users/hector/SeatServe/seatserve-backend/
```

That backend uses:
- **FastAPI** framework (not Django)
- **SQLite** database
- **Stripe** integration for payments
- Direct API endpoints for payment processing

This `backend/` directory contains Django models that could be used for:
1. Future Django migration
2. Reference implementation
3. Database schema documentation
4. Alternative backend architecture

## Usage Notes

⚠️ **Important:** These models are **not currently active** in the running application. The active payment processing uses the FastAPI backend in `seatserve-backend/`.

To use these models, you would need to:
1. Set up a Django project
2. Configure database settings
3. Run migrations
4. Integrate with the existing Stripe payment flow

## Related Documentation

For the **active backend** documentation, see:
- `/Users/hector/SeatServe/seatserve-backend/README.md` (to be created)
- `/Users/hector/SeatServe/seatserve-backend/STRIPE_SETUP.md`

## Model Features

### Database Optimization
- Indexed fields for fast queries
- Composite indexes on user and creation date
- Status and payment intent ID indexes

### Data Integrity
- Foreign key constraints
- Unique constraints on Stripe IDs
- Automatic timestamp management

### Audit Trail
- Complete payment history via PaymentLog
- Stores raw Stripe responses
- Error tracking and debugging support

## Future Considerations

If migrating to Django:
1. Create Django project and app
2. Copy these models to Django app
3. Create Order model (referenced but not defined here)
4. Configure Stripe webhooks
5. Run migrations
6. Update frontend to use new endpoints

## Model Field Reference

### Payment Model Fields

#### Relationships
- `order` - OneToOne link to Order model
- `user` - ForeignKey to Django User model (nullable)

#### Stripe Fields
- `stripe_payment_intent_id` - Unique Stripe Payment Intent ID
- `stripe_charge_id` - Unique Stripe Charge ID (nullable)
- `stripe_customer_id` - Stripe Customer ID for recurring customers

#### Financial Fields
- `amount` - Payment amount (Decimal, 10 digits, 2 decimal places)
- `currency` - Currency code (default: USD, 3 characters)
- `refund_amount` - Total amount refunded (Decimal, default: 0)

#### Payment Information
- `payment_method` - Payment method used (card, paypal, apple_pay, google_pay)
- `status` - Payment status (pending, succeeded, failed, canceled, refunded)

#### Card Information
- `card_last_four` - Last 4 digits of card number
- `card_brand` - Card brand (visa, mastercard, amex, discover)
- `card_exp_month` - Card expiration month (1-12)
- `card_exp_year` - Card expiration year (4 digits)

#### Metadata
- `description` - Payment description
- `receipt_url` - URL to Stripe receipt
- `receipt_email` - Email where receipt was sent
- `refund_reason` - Reason for refund (if applicable)

#### Timestamps
- `created_at` - When payment record was created (auto)
- `updated_at` - Last update timestamp (auto)
- `paid_at` - When payment was successfully completed
- `refunded_at` - When refund was processed (if applicable)

### PaymentLog Model Fields

- `payment` - ForeignKey to Payment model
- `event_type` - Type of event logged (choices from EVENTS)
- `data` - Complete JSON data from Stripe webhook/response
- `error_message` - Error message if event_type is 'error'
- `created_at` - Timestamp of log entry (auto)

## Code Examples

### Creating a Payment Record

```python
from app.models.payment import Payment
from decimal import Decimal

payment = Payment.objects.create(
    order=order_instance,
    user=user_instance,
    stripe_payment_intent_id="pi_1234567890",
    amount=Decimal('25.99'),
    currency='USD',
    payment_method='card',
    status='pending'
)
```

### Logging Payment Events

```python
from app.models.payment import PaymentLog

PaymentLog.objects.create(
    payment=payment_instance,
    event_type='intent_created',
    data=stripe_response_data
)
```

### Querying Payments

```python
# Get all successful payments for a user
successful_payments = Payment.objects.filter(
    user=user_instance,
    status='succeeded'
)

# Get all payments that can be refunded
refundable = Payment.objects.filter(
    status='succeeded',
    refund_amount=0
)

# Get payment with all logs
payment = Payment.objects.prefetch_related('logs').get(id=payment_id)
for log in payment.logs.all():
    print(f"{log.event_type}: {log.created_at}")
```

## Database Schema SQL

### Payment Table
```sql
CREATE TABLE payment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL UNIQUE,
    user_id INTEGER,
    stripe_payment_intent_id VARCHAR(255) UNIQUE NOT NULL,
    stripe_charge_id VARCHAR(255) UNIQUE,
    stripe_customer_id VARCHAR(255),
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    payment_method VARCHAR(20) DEFAULT 'card',
    status VARCHAR(20) DEFAULT 'pending',
    card_last_four VARCHAR(4),
    card_brand VARCHAR(50),
    card_exp_month INTEGER,
    card_exp_year INTEGER,
    description TEXT,
    receipt_url TEXT,
    receipt_email VARCHAR(254),
    refund_amount DECIMAL(10, 2) DEFAULT 0,
    refund_reason VARCHAR(255),
    refunded_at DATETIME,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    paid_at DATETIME,
    FOREIGN KEY (order_id) REFERENCES order(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE SET NULL
);

CREATE INDEX idx_payment_user_created ON payment(user_id, created_at DESC);
CREATE INDEX idx_payment_status ON payment(status);
CREATE INDEX idx_payment_intent ON payment(stripe_payment_intent_id);
```

### PaymentLog Table
```sql
CREATE TABLE payment_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    payment_id INTEGER NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    data JSON DEFAULT '{}',
    error_message TEXT,
    created_at DATETIME NOT NULL,
    FOREIGN KEY (payment_id) REFERENCES payment(id) ON DELETE CASCADE
);

CREATE INDEX idx_paymentlog_created ON payment_log(created_at DESC);
```

## Integration with Stripe Webhooks

While not currently implemented, here's how these models would integrate with Stripe webhooks:

### Webhook Handler Example

```python
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import stripe
import json

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
        
        # Handle payment_intent.succeeded
        if event['type'] == 'payment_intent.succeeded':
            intent = event['data']['object']
            payment = Payment.objects.get(
                stripe_payment_intent_id=intent['id']
            )
            payment.status = 'succeeded'
            payment.paid_at = timezone.now()
            payment.save()
            
            # Log the event
            PaymentLog.objects.create(
                payment=payment,
                event_type='intent_succeeded',
                data=event['data']['object']
            )
        
        return JsonResponse({'status': 'success'})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
```

## Development Status

**Status:** ✅ **COMPLETED**

- ✅ Models defined and documented
- ✅ Payment model implementation complete
- ✅ PaymentLog model for audit trail
- ✅ Database optimization with indexes
- ✅ Comprehensive field documentation
- ✅ Code examples and SQL schemas
- ❌ Not integrated with active application (Django models for future use)
- ❌ No Django project configured
- ❌ No migrations created

---

**Status:** ✅ **COMPLETED**

Built with ❤️ by Héctor Soto & Alejandro Garcia

---

**Note:** For current backend operations, always refer to the FastAPI backend in `/Users/hector/SeatServe/seatserve-backend/`
