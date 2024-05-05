from django.urls import path
from .views import train_classifier
from . import views

urlpatterns = [
    path('predictions/', views.train_classifier, name='predictions'),
    path('backoffice/', views.backoffice, name='backoffice'),
    path('train/', train_classifier, name='train_classifier'),
]
