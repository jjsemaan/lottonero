from django.urls import path
from .views import run_scrape_euromillions

urlpatterns = [
    path('run-scrape/', run_scrape_euromillions, name='run_scrape_euromillions'),
]
