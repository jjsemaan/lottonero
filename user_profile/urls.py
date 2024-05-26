from django.urls import path
from user_profile.views import SignUpView

urlpatterns = [
    path('signUpView/', SignUpView.as_view(), name='signUpView'),
]