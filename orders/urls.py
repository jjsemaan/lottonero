from django.urls import path
from .views import subscription_types_view

urlpatterns = [
    path('orders/', subscription_types_view, name='plans'),
]
