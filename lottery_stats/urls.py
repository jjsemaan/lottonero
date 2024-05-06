from django.urls import path
from . import views

urlpatterns = [
    path('frequencies/', views.frequency_view, name='frequencies'),
    path('combinations/', views.combinations_view, name='combinations'),
    path('correlations/', views.correlations_view, name='correlations'),
]
