from django.db import models
from django.contrib.auth.models import User
from .order import Order


class Payment(models.Model):
    """
    Model to store Stripe payment transaction history
    """
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('succeeded', 'Succeeded'),
        ('failed', 'Failed'),
        ('canceled', 'Canceled'),
        ('refunded', 'Refunded'),
    ]

    PAYMENT_METHOD = [
        ('card', 'Credit/Debit Card'),
        ('paypal', 'PayPal'),
        ('apple_pay', 'Apple Pay'),
        ('google_pay', 'Google Pay'),
    ]

    # Order information
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='payments')

    # Stripe information
    stripe_payment_intent_id = models.CharField(max_length=255, unique=True)
    stripe_charge_id = models.CharField(max_length=255, null=True, blank=True, unique=True)
    stripe_customer_id = models.CharField(max_length=255, null=True, blank=True)

    # Payment details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD, default='card')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')

    # Card information
    card_last_four = models.CharField(max_length=4, null=True, blank=True)
    card_brand = models.CharField(max_length=50, null=True, blank=True)  # visa, mastercard, etc.
    card_exp_month = models.IntegerField(null=True, blank=True)
    card_exp_year = models.IntegerField(null=True, blank=True)

    # Metadata
    description = models.TextField(null=True, blank=True)
    receipt_url = models.URLField(null=True, blank=True)
    receipt_email = models.EmailField(null=True, blank=True)

    # Refunds
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    refund_reason = models.CharField(max_length=255, null=True, blank=True)
    refunded_at = models.DateTimeField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['stripe_payment_intent_id']),
        ]

    def __str__(self):
        return f"Payment {self.stripe_payment_intent_id} - {self.amount} {self.currency}"

    def is_paid(self):
        return self.status == 'succeeded'

    def can_refund(self):
        return self.is_paid() and self.refund_amount == 0


class PaymentLog(models.Model):
    """
    Detailed log of each payment event for debugging and auditing
    """
    EVENTS = [
        ('intent_created', 'Payment Intent Created'),
        ('intent_succeeded', 'Payment Intent Succeeded'),
        ('intent_failed', 'Payment Intent Failed'),
        ('charge_created', 'Charge Created'),
        ('refund_created', 'Refund Created'),
        ('webhook_received', 'Webhook Received'),
        ('error', 'Error'),
    ]

    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='logs')
    event_type = models.CharField(max_length=50, choices=EVENTS)
    data = models.JSONField(default=dict)  # Stores complete Stripe response
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.payment} - {self.event_type}"
