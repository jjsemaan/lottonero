from django.urls import path
from . import views

urlpatterns = [
    path("profile/", views.profile_view, name="profile_view"),
    path("profile/update/", views.update_profile, name="update_profile"),
    path(
        "profile/change_password/",
        views.change_password,
        name="change_password",
    ),
    path(
        "terms-and-conditions/",
        views.terms_and_conditions,
        name="terms_and_conditions",
    ),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
]
