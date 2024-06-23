from django.urls import path

from . import views

urlpatterns = [
    path(
        "run-scrape/",
        views.run_scrape_euromillions,
        name="run_scrape_euromillions",
    )
]
