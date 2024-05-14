from django.contrib import admin
from django.urls import path
from .views import index, latest_predictions_with_matches

urlpatterns = [
    path('', index, name='home'),  # Homepage pointing to index
    path('latest-predictions-with-matches/', latest_predictions_with_matches, name='latest_predictions_with_matches'),  # Endpoint for updating matches
]
