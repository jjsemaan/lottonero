# webhook_handler.py
import stripe
from django.conf import settings
from djstripe.models import Customer, Subscription, Product, Price

stripe.api_key = settings.STRIPE_SECRET_KEY

def handle_checkout_session_completed(session):
    client_reference_id = session.get('client_reference_id')
    subscription_id = session.get('subscription')

    if client_reference_id and subscription_id:
        user = get_user_model().objects.get(id=client_reference_id)
        subscription = stripe.Subscription.retrieve(subscription_id)
        djstripe_subscription = Subscription.sync_from_stripe_data(subscription)

        # Sync products and prices
        for item in subscription['items']['data']:
            plan = item['plan']
            product = plan['product']
            price = plan

            if isinstance(product, str):
                product = stripe.Product.retrieve(product)
            if isinstance(price, str):
                price = stripe.Price.retrieve(price)

            djstripe_product = Product.sync_from_stripe_data(product)
            djstripe_price = Price.sync_from_stripe_data(price)

            if djstripe_product.default_price != djstripe_price:
                djstripe_product.default_price = djstripe_price
                djstripe_product.save()

        djstripe_subscription.customer = Customer.sync_from_stripe_data(user)
        djstripe_subscription.save()

def handle_payment_intent_succeeded(payment_intent):
    # Custom logic for handling successful payment intents
    print(f"Payment for {payment_intent['amount']} succeeded.")

def handle_payment_method_attached(payment_method):
    # Custom logic for handling successful attachment of a payment method
    print(f"Payment method {payment_method['id']} attached.")
