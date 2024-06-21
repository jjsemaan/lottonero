from django.urls import path
from . import views
from .webhook import stripe_webhook
from .webhooks import webhook

urlpatterns = [
    path("pricing-page/", views.pricing_page, name="pricing_page"),
    path("subscription-confirm/", views.subscription_confirm, name="subscription_confirm"),
    path('stripe/webhook/', stripe_webhook, name='stripe-webhook'),
    path('wh/', webhook, name='webhook'),
]