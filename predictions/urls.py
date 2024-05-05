from django.urls import path
from .views import train_classifier
from .views import display_predictions
from . import views

urlpatterns = [
    path('predictions/', display_predictions, name='predictions'),
    path('backoffice/', views.backoffice, name='backoffice'),
    path('train/', train_classifier, name='train_classifier'),
]