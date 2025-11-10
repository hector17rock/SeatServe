# SeatServe Backend (Django Models)

This directory contains Django model definitions for the SeatServe payment system. This is a **separate** backend from the main FastAPI application.

## Author

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

## Development Status

- ✅ Models defined and documented
- ❌ Not integrated with active application
- ❌ No Django project configured
- ❌ No migrations created

---

**Note:** For current backend operations, always refer to the FastAPI backend in `/Users/hector/SeatServe/seatserve-backend/`
