from django.urls import path
from .views import subscription_types_view
from . import views

urlpatterns = [
    path('orders/', subscription_types_view, name='plans'),
    path('checkout/<int:subscription_id>/', views.checkout, name='checkout'),
    path('subscription_success/', views.subscription_success, name='subscription_success'),
]
