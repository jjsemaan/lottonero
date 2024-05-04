from django.contrib import admin
from django.urls import path
from .views import latest_draw
from .import views

urlpatterns = [
    path('', views.latest_draw, name='home'),  # Make sure this points to latest_draw for the homepage
    path('latest-draw/', views.latest_draw, name='latest_draw'),  # Optional: This can be removed if you don't need a separate URL
]