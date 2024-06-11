from django.urls import path

from . import views

urlpatterns = [
    path('run-scrape/', views.run_scrape_euromillions, name='run_scrape_euromillions'),
    path('backoffice-success/', views.backoffice_success, name='backoffice_success'),
    path('backoffice-failed/', views.backoffice_failed, name='backoffice_failed'),
]
