from django.urls import path
from . import views

urlpatterns = [
    path('backoffice', views.backoffice_home, name='backoffice_home'),
]
