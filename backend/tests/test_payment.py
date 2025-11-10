"""
Unit tests for Payment and PaymentLog models

Tests cover:
1. Payment model creation with all required fields and default values
2. Payment.is_paid() method correctness
3. Payment.can_refund() method correctness
4. PaymentLog model creation and JSON data storage
5. Unique constraint enforcement for stripe_payment_intent_id
"""

import pytest
from decimal import Decimal
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.test import TestCase
from unittest.mock import MagicMock, patch, Mock

# Import the models
from app.models.payment import Payment, PaymentLog
from app.models.order import Order


@pytest.mark.django_db
class TestPaymentModelCreation(TestCase):
    """Test suite for Payment model creation and field initialization"""

    def setUp(self):
        """Set up test fixtures"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.order = Order.objects.create()

    def test_payment_creation_with_all_required_fields(self):
        """
        Test 1: Payment model can be created with all required fields
        and default values are set correctly
        """
        payment = Payment.objects.create(
            order=self.order,
            user=self.user,
            stripe_payment_intent_id='pi_test_123456',
            stripe_charge_id='ch_test_123456',
            amount=Decimal('99.99'),
            currency='USD',
            payment_method='card',
            status='succeeded'
        )

        # Verify all fields are stored correctly
        assert payment.id is not None
        assert payment.order == self.order
        assert payment.user == self.user
        assert payment.stripe_payment_intent_id == 'pi_test_123456'
        assert payment.stripe_charge_id == 'ch_test_123456'
        assert payment.amount == Decimal('99.99')
        assert payment.currency == 'USD'
        assert payment.payment_method == 'card'
        assert payment.status == 'succeeded'

    def test_payment_default_values(self):
        """
        Test that default values are properly set when not explicitly provided
        """
        payment = Payment.objects.create(
            order=self.order,
            user=self.user,
            stripe_payment_intent_id='pi_default_test_123',
            amount=Decimal('50.00')
        )

        # Verify default values
        assert payment.currency == 'USD'
        assert payment.payment_method == 'card'
        assert payment.status == 'pending'
        assert payment.refund_amount == Decimal('0.00')
        assert payment.card_last_four is None
        assert payment.card_brand is None
        assert payment.created_at is not None
        assert payment.updated_at is not None

    def test_payment_optional_fields(self):
        """
        Test that optional fields can be set and retrieved correctly
        """
        payment = Payment.objects.create(
            order=self.order,
            user=self.user,
            stripe_payment_intent_id='pi_optional_test_123',
            amount=Decimal('75.50'),
            card_last_four='4242',
            card_brand='Visa',
            card_exp_month=12,
            card_exp_year=2025,
            description='Test payment for order #1',
            receipt_email='receipt@example.com'
        )

        # Verify optional fields
        assert payment.card_last_four == '4242'
        assert payment.card_brand == 'Visa'
        assert payment.card_exp_month == 12
        assert payment.card_exp_year == 2025
        assert payment.description == 'Test payment for order #1'
        assert payment.receipt_email == 'receipt@example.com'

    def test_payment_with_all_payment_methods(self):
        """
        Test that all supported payment methods can be assigned
        """
        payment_methods = ['card', 'paypal', 'apple_pay', 'google_pay']
        
        for idx, method in enumerate(payment_methods):
            order = Order.objects.create()  # Create new order for each payment
            payment = Payment.objects.create(
                order=order,
                user=self.user,
                stripe_payment_intent_id=f'pi_method_{method}_{idx}',
                amount=Decimal('25.00'),
                payment_method=method
            )
            assert payment.payment_method == method


@pytest.mark.django_db
class TestPaymentIsPaidMethod(TestCase):
    """Test suite for Payment.is_paid() method"""

    def setUp(self):
        """Set up test fixtures"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.order = Order.objects.create()
        self.order.id = 1

    def test_is_paid_returns_true_for_succeeded_status(self):
        """
        Test 2: Payment.is_paid() correctly identifies a successful payment
        """
        payment = Payment.objects.create(
            order=self.order,
            user=self.user,
            stripe_payment_intent_id='pi_paid_test_123',
            amount=Decimal('100.00'),
            status='succeeded'
        )

        assert payment.is_paid() is True

    def test_is_paid_returns_false_for_pending_status(self):
        """
        Test that is_paid() returns False for pending payments
        """
        payment = Payment.objects.create(
            order=self.order,
            user=self.user,
            stripe_payment_intent_id='pi_pending_test_123',
            amount=Decimal('100.00'),
            status='pending'
        )

        assert payment.is_paid() is False

    def test_is_paid_returns_false_for_failed_status(self):
        """
        Test that is_paid() returns False for failed payments
        """
        payment = Payment.objects.create(
            order=self.order,
            user=self.user,
            stripe_payment_intent_id='pi_failed_test_123',
            amount=Decimal('100.00'),
            status='failed'
        )

        assert payment.is_paid() is False

    def test_is_paid_returns_false_for_canceled_status(self):
        """
        Test that is_paid() returns False for canceled payments
        """
        payment = Payment.objects.create(
            order=self.order,
            user=self.user,
            stripe_payment_intent_id='pi_canceled_test_123',
            amount=Decimal('100.00'),
            status='canceled'
        )

        assert payment.is_paid() is False

    def test_is_paid_returns_false_for_refunded_status(self):
        """
        Test that is_paid() returns False for refunded payments
        """
        payment = Payment.objects.create(
            order=self.order,
            user=self.user,
            stripe_payment_intent_id='pi_refunded_test_123',
            amount=Decimal('100.00'),
            status='refunded'
        )

        assert payment.is_paid() is False


@pytest.mark.django_db
class TestPaymentCanRefundMethod(TestCase):
    """Test suite for Payment.can_refund() method"""

    def setUp(self):
        """Set up test fixtures"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.order = Order.objects.create()
        self.order.id = 1

    def test_can_refund_returns_true_for_paid_with_zero_refund(self):
        """
        Test 3: Payment.can_refund() correctly determines if a payment can be refunded
        A payment can be refunded if it's succeeded and no refund has been issued
        """
        payment = Payment.objects.create(
            order=self.order,
            user=self.user,
            stripe_payment_intent_id='pi_refundable_test_123',
            amount=Decimal('100.00'),
            status='succeeded',
            refund_amount=Decimal('0.00')
        )

        assert payment.can_refund() is True

    def test_can_refund_returns_false_for_pending_payment(self):
        """
        Test that can_refund() returns False for pending payments
        """
        payment = Payment.objects.create(
            order=self.order,
            user=self.user,
            stripe_payment_intent_id='pi_pending_refund_test_123',
            amount=Decimal('100.00'),
            status='pending',
            refund_amount=Decimal('0.00')
        )

        assert payment.can_refund() is False

    def test_can_refund_returns_false_for_payment_with_existing_refund(self):
        """
        Test that can_refund() returns False if refund has already been issued
        """
        payment = Payment.objects.create(
            order=self.order,
            user=self.user,
            stripe_payment_intent_id='pi_partially_refunded_test_123',
            amount=Decimal('100.00'),
            status='succeeded',
            refund_amount=Decimal('50.00')
        )

        assert payment.can_refund() is False

    def test_can_refund_returns_false_for_failed_payment(self):
        """
        Test that can_refund() returns False for failed payments
        """
        payment = Payment.objects.create(
            order=self.order,
            user=self.user,
            stripe_payment_intent_id='pi_failed_refund_test_123',
            amount=Decimal('100.00'),
            status='failed',
            refund_amount=Decimal('0.00')
        )

        assert payment.can_refund() is False

    def test_can_refund_returns_false_for_fully_refunded_payment(self):
        """
        Test that can_refund() returns False when payment is fully refunded
        """
        payment = Payment.objects.create(
            order=self.order,
            user=self.user,
            stripe_payment_intent_id='pi_fully_refunded_test_123',
            amount=Decimal('100.00'),
            status='succeeded',
            refund_amount=Decimal('100.00')
        )

        assert payment.can_refund() is False


@pytest.mark.django_db
class TestPaymentLogModel(TestCase):
    """Test suite for PaymentLog model"""

    def setUp(self):
        """Set up test fixtures"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.order = Order.objects.create()
        self.order.id = 1
        self.payment = Payment.objects.create(
            order=self.order,
            user=self.user,
            stripe_payment_intent_id='pi_log_test_123',
            amount=Decimal('100.00'),
            status='pending'
        )

    def test_payment_log_creation(self):
        """
        Test 4: PaymentLog model can be created and stores event data as JSON
        """
        log_data = {
            'event_id': 'evt_123456',
            'created': 1234567890,
            'type': 'payment_intent.succeeded',
            'data': {
                'object': {
                    'id': 'pi_log_test_123',
                    'amount': 10000,
                    'status': 'succeeded'
                }
            }
        }

        log = PaymentLog.objects.create(
            payment=self.payment,
            event_type='intent_succeeded',
            data=log_data
        )

        assert log.id is not None
        assert log.payment == self.payment
        assert log.event_type == 'intent_succeeded'
        assert log.data == log_data
        assert log.error_message is None
        assert log.created_at is not None

    def test_payment_log_stores_complex_json_data(self):
        """
        Test that PaymentLog correctly stores complex nested JSON data
        """
        complex_data = {
            'charge': {
                'id': 'ch_123456',
                'amount': 10000,
                'currency': 'usd',
                'payment_method_details': {
                    'card': {
                        'last4': '4242',
                        'brand': 'visa',
                        'exp_month': 12,
                        'exp_year': 2025
                    }
                }
            },
            'metadata': {
                'order_id': '12345',
                'customer_id': '67890'
            }
        }

        log = PaymentLog.objects.create(
            payment=self.payment,
            event_type='charge_created',
            data=complex_data
        )

        retrieved_log = PaymentLog.objects.get(id=log.id)
        assert retrieved_log.data == complex_data
        assert retrieved_log.data['charge']['id'] == 'ch_123456'
        assert retrieved_log.data['metadata']['order_id'] == '12345'

    def test_payment_log_with_error_message(self):
        """
        Test that PaymentLog can store error messages
        """
        error_data = {
            'error_code': 'authentication_error',
            'message': 'Card authentication failed'
        }

        log = PaymentLog.objects.create(
            payment=self.payment,
            event_type='error',
            data=error_data,
            error_message='Your card was declined. Please try another payment method.'
        )

        assert log.event_type == 'error'
        assert log.error_message == 'Your card was declined. Please try another payment method.'
        assert log.data['error_code'] == 'authentication_error'

    def test_payment_log_all_event_types(self):
        """
        Test that all supported event types can be used
        """
        event_types = [
            'intent_created',
            'intent_succeeded',
            'intent_failed',
            'charge_created',
            'refund_created',
            'webhook_received',
            'error'
        ]

        for idx, event_type in enumerate(event_types):
            log = PaymentLog.objects.create(
                payment=self.payment,
                event_type=event_type,
                data={'event_index': idx}
            )
            assert log.event_type == event_type

    def test_payment_log_relationship_cascade_delete(self):
        """
        Test that PaymentLogs are deleted when Payment is deleted
        """
        log = PaymentLog.objects.create(
            payment=self.payment,
            event_type='intent_created',
            data={'test': 'data'}
        )

        log_id = log.id
        self.payment.delete()

        # Verify log was deleted
        assert not PaymentLog.objects.filter(id=log_id).exists()


@pytest.mark.django_db
class TestPaymentUniqueConstraints(TestCase):
    """Test suite for Payment model unique constraints"""

    def setUp(self):
        """Set up test fixtures"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.order = Order.objects.create()
        self.order.id = 1

    def test_stripe_payment_intent_id_unique_constraint(self):
        """
        Test 5: Payment model enforces unique constraint for stripe_payment_intent_id
        Attempting to create a second payment with the same intent ID should raise IntegrityError
        """
        intent_id = 'pi_unique_constraint_test_123'

        # Create first payment
        payment1 = Payment.objects.create(
            order=self.order,
            user=self.user,
            stripe_payment_intent_id=intent_id,
            amount=Decimal('100.00')
        )

        # Attempt to create second payment with same intent ID
        with pytest.raises(IntegrityError):
            Payment.objects.create(
                order=self.order,
                user=self.user,
                stripe_payment_intent_id=intent_id,
                amount=Decimal('100.00')
            )

    def test_stripe_charge_id_unique_constraint(self):
        """
        Test that stripe_charge_id also enforces uniqueness
        """
        charge_id = 'ch_unique_constraint_test_123'
        order2 = Order.objects.create()

        # Create first payment with charge ID
        payment1 = Payment.objects.create(
            order=self.order,
            user=self.user,
            stripe_payment_intent_id='pi_unique_charge_1',
            stripe_charge_id=charge_id,
            amount=Decimal('100.00')
        )

        # Attempt to create second payment with same charge ID
        with pytest.raises(IntegrityError):
            Payment.objects.create(
                order=order2,
                user=self.user,
                stripe_payment_intent_id='pi_unique_charge_2',
                stripe_charge_id=charge_id,
                amount=Decimal('100.00')
            )

    def test_multiple_payments_same_user_different_intent_ids(self):
        """
        Test that same user can have multiple payments with different intent IDs
        """
        order1 = Order.objects.create()
        order2 = Order.objects.create()
        
        payment1 = Payment.objects.create(
            order=order1,
            user=self.user,
            stripe_payment_intent_id='pi_user_multi_1',
            amount=Decimal('100.00')
        )

        payment2 = Payment.objects.create(
            order=order2,
            user=self.user,
            stripe_payment_intent_id='pi_user_multi_2',
            amount=Decimal('50.00')
        )

        assert payment1.user == payment2.user
        assert payment1.stripe_payment_intent_id != payment2.stripe_payment_intent_id
        assert Payment.objects.filter(user=self.user).count() == 2


@pytest.mark.django_db
class TestPaymentModelStringRepresentation(TestCase):
    """Test suite for Payment model string representation and metadata"""

    def setUp(self):
        """Set up test fixtures"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.order = Order.objects.create()
        self.order.id = 1

    def test_payment_string_representation(self):
        """
        Test that __str__ returns expected format
        """
        payment = Payment.objects.create(
            order=self.order,
            user=self.user,
            stripe_payment_intent_id='pi_str_test_123',
            amount=Decimal('99.99'),
            currency='USD'
        )

        expected_str = f"Payment pi_str_test_123 - 99.99 USD"
        assert str(payment) == expected_str

    def test_payment_log_string_representation(self):
        """
        Test that PaymentLog __str__ returns expected format
        """
        payment = Payment.objects.create(
            order=self.order,
            user=self.user,
            stripe_payment_intent_id='pi_log_str_test_123',
            amount=Decimal('100.00')
        )

        log = PaymentLog.objects.create(
            payment=payment,
            event_type='intent_succeeded',
            data={'test': 'data'}
        )

        assert 'pi_log_str_test_123' in str(log)
        assert 'intent_succeeded' in str(log)


# Test runner configuration
if __name__ == '__main__':
    pytest.main([__file__, '-v'])
