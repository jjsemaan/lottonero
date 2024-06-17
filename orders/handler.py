# handler.py
import stripe
from django.conf import settings
from djstripe.models import Customer, Subscription, Product, Price
from django.contrib.auth import get_user_model

stripe.api_key = settings.STRIPE_SECRET_KEY

def handle_checkout_session_completed(session):
    # Placeholder for existing logic
    pass  # Replace 'pass' with actual logic

def handle_payment_intent_succeeded(payment_intent):
    # Placeholder for existing logic
    pass  # Replace 'pass' with actual logic

def handle_payment_method_attached(payment_method):
    # Placeholder for existing logic
    pass  # Replace 'pass' with actual logic

def handle_subscription_created(subscription):
    djstripe_subscription = Subscription.sync_from_stripe_data(subscription)
    print(f"Subscription {djstripe_subscription.id} created for customer {djstripe_subscription.customer}")

def handle_subscription_updated(subscription):
    djstripe_subscription = Subscription.sync_from_stripe_data(subscription)
    print(f"Subscription {djstripe_subscription.id} updated for customer {djstripe_subscription.customer}")
