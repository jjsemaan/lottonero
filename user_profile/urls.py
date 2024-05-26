from django.urls import path
from .views import display_predictions
from home.views import latest_predictions_with_matches
from . import views

urlpatterns = [
    path('predictions/', display_predictions, name='predictions'),
    path('backoffice/', views.backoffice, name='backoffice'),
    path('train/', train_classifier, name='train_classifier'),
    path('check-winning-predictions/', latest_predictions_with_matches, name='latest_predictions_with_matches'),
]