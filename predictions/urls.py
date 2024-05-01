from django.urls import path
from . import views

urlpatterns = [
    path('predictions/', views.train_classifier, name='predictions'),
]
