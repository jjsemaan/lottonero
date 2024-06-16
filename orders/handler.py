import stripe
from django.contrib.auth import get_user_model
from djstripe.models import Customer, Subscription, Product, Price

def handle_checkout_session(session):
    client_reference_id = session.get('client_reference_id')
    subscription_id = session.get('subscription')

    print(f"client_reference_id: {client_reference_id}, subscription_id: {subscription_id}")

    if client_reference_id and subscription_id:
        try:
            user = get_user_model().objects.get(id=client_reference_id)
            subscription = stripe.Subscription.retrieve(subscription_id)
            djstripe_subscription = Subscription.sync_from_stripe_data(subscription)

            # Sync products and prices
            for item in subscription.items.data:
                plan = item.plan
                product = plan.product
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

            # Link the subscription with the user
            djstripe_subscription.customer = Customer.sync_from_stripe_data(user)
            djstripe_subscription.save()
        except Exception as e:
            print(f"Error handling checkout session: {e}")
