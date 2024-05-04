from django.contrib import admin
from django.urls import path
from .views import latest_draw
from .import views

urlpatterns = [
    path('', views.index, name='home'),
    path('latest-draw/', views.latest_draw, name='latest_draw'),
]