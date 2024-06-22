import stripe
from django.http import HttpResponse
from django.conf import settings
from djstripe.models import Customer, Subscription, Product, Price
from django.contrib.auth import get_user_model


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}', status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}', status=200
        )

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}', status=200
        )

    def handle_checkout_session_completed(session):
        # Placeholder for existing logic
        return HttpResponse(
            content=f'Webhook received: {event["type"]}', status=200
        )

    def handle_subscription_created(subscription):
        djstripe_subscription = Subscription.sync_from_stripe_data(
            subscription
        )
        print(
            f"Subscription {djstripe_subscription.id} created for customer {djstripe_subscription.customer}"
        )

    def handle_subscription_updated(subscription):
        djstripe_subscription = Subscription.sync_from_stripe_data(
            subscription
        )
        print(
            f"Subscription {djstripe_subscription.id} updated for customer {djstripe_subscription.customer}"
        )
