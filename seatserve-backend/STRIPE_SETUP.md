# Stripe Integration Setup Guide

This guide will help you set up Stripe payment processing for SeatServe.

## Prerequisites

- Python 3.8+ with virtual environment
- Stripe account (sign up at https://stripe.com)
- All required packages are already installed in the virtual environment

## Step 1: Get Your Stripe API Keys

1. Go to https://dashboard.stripe.com/test/apikeys
2. Sign in or create a Stripe account
3. Copy your **Publishable key** (starts with `pk_test_`)
4. Click "Reveal test key" and copy your **Secret key** (starts with `sk_test_`)

## Step 2: Configure Environment Variables

1. Open `/Users/hector/SeatServe/seatserve-backend/.env`
2. Replace the placeholder keys with your actual Stripe keys:

```env
STRIPE_SECRET_KEY=sk_test_your_actual_secret_key_here
STRIPE_PUBLISHABLE_KEY=pk_test_your_actual_publishable_key_here
```

## Step 3: Start the Backend Server

```bash
cd /Users/hector/SeatServe/seatserve-backend
source venv/bin/activate
python main.py
```

The server will start on http://localhost:8000

## Step 4: Test the Integration

1. Open your frontend application
2. Add items to cart and proceed to checkout
3. Use Stripe test card numbers:
   - **Successful payment**: `4242 4242 4242 4242`
   - **Requires authentication**: `4000 0025 0000 3155`
   - **Declined payment**: `4000 0000 0000 9995`
   
4. For expiration date, use any future date (e.g., 12/34)
5. For CVV, use any 3 digits (e.g., 123)
6. For ZIP code, use any 5 digits (e.g., 12345)

## API Endpoints

### Get Stripe Configuration
```
GET /api/stripe/config
```
Returns the Stripe publishable key for the frontend.

### Create Payment Intent
```
POST /api/stripe/create-payment-intent
Content-Type: application/json

{
  "amount": 25.50,
  "order_data": { ... }
}
```
Creates a Stripe Payment Intent and returns the client secret.

### Webhook Handler (Optional)
```
POST /api/stripe/webhook
```
Handles Stripe webhook events for payment confirmations.

## Security Notes

- **Never commit your `.env` file** to version control
- Use test keys during development (they start with `sk_test_` and `pk_test_`)
- Switch to live keys only when ready for production (they start with `sk_live_` and `pk_live_`)
- The `.env` file is already in `.gitignore`

## Troubleshooting

### "Payment system not configured" error
- Check that your Stripe keys are properly set in `.env`
- Make sure the backend server is running
- Verify the backend URL in checkout.html matches your server (default: http://localhost:8000)

### Card element not showing
- Check browser console for errors
- Ensure Stripe.js is loading properly
- Verify your publishable key is correct

### Payment fails immediately
- Check that your secret key is correct
- Look at backend logs for error messages
- Try using a different test card number

## Additional Resources

- [Stripe Testing Guide](https://stripe.com/docs/testing)
- [Stripe Payment Intents API](https://stripe.com/docs/payments/payment-intents)
- [Stripe Elements](https://stripe.com/docs/stripe-js)

## Support

If you encounter issues:
1. Check the backend logs in the terminal
2. Check browser console for frontend errors
3. Verify all Stripe keys are correct and not expired
4. Ensure you're using test mode keys during development
