from django.urls import path
from . import views
from .views import cancel_subscription_view
from .webhook import stripe_webhook

urlpatterns = [
    path("pricing-page/", views.pricing_page, name="pricing_page"),
    path(
        "subscription-confirm/",
        views.subscription_confirm,
        name="subscription_confirm",
    ),
    path("stripe/webhook/", stripe_webhook, name="stripe-webhook"),
    path(
        "subscriptions/cancel/<int:subscription_id>/",
        cancel_subscription_view,
        name="cancel_subscription",
    ),
]