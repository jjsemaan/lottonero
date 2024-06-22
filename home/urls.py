from django.contrib import admin
from django.urls import path
from .views import (
    index,
    latest_predictions_with_matches,
    alltime_winning_predictions_view,
    latest_shuffled_predictions_with_matches,
)

urlpatterns = [
    path("", index, name="home"),
    path(
        "latest-predictions-with-matches/",
        latest_predictions_with_matches,
        name="latest_predictions_with_matches",
    ),
    path(
        "alltime/",
        alltime_winning_predictions_view,
        name="alltime_predictions",
    ),
    path(
        "latest-shuffled-predictions-with-matches/",
        latest_shuffled_predictions_with_matches,
        name="latest_combination_predictions_with_matches",
    ),
]
