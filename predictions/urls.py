from django.urls import path
from .views import train_classifier, display_predictions, upload_image, upload_success
from home.views import latest_predictions_with_matches
from . import views

urlpatterns = [
    path('predictions/', display_predictions, name='predictions'),
    path('backoffice/', views.backoffice, name='backoffice'),
    path('train/', train_classifier, name='train_classifier'),
    path('check-winning-predictions/', latest_predictions_with_matches, name='latest_predictions_with_matches'),
    path('upload/', upload_image, name='upload_image'),
    path('upload_success/', upload_success, name='upload_success'),
]
