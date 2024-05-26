from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, CreateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy

from .forms import SignUpForm, UserForm, ProfileForm
from .models import Profile


class SignUpView(CreateView):
    """
    Handles user registration using a custom SignUp form. Upon successful
    registration, redirects to the login page with a success message.
    If registration fails, it displays error messages.
    """
    form_class = SignUpForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            "Your account has been created successfully! You can now log in.",
        )
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(
            self.request, "Registration failed. Correct the errors below."
        )
        return response


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    Displays the user profile page.
    """
    template_name = "customer/profile.html"


class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    """
    Allows users to update their profile information including basic user data
    and profile details.Saves the form data and redirects to the profile page
    on successful update or re-renders the form on errors.
    """
    user_form = UserForm
    profile_form = ProfileForm
    template_name = "customer/profile-update.html"

    def post(self, request):

        post_data = request.POST or None

        user_form = UserForm(post_data, instance=request.user)
        profile_form = ProfileForm(post_data, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile is updated successfully!")
            return HttpResponseRedirect(reverse_lazy("profile"))

        context = self.get_context_data(
            user_form=user_form, profile_form=profile_form
        )

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class CustomLoginView(LoginView):
    """
    Customized login view that displays success or error messages based on the
    login attempt's outcome.
    """
    template_name = "registration/login.html"
    redirect_authenticated_user = False

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Login Successful! Welcome back.")
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(
            self.request,
            "Login failed. Check your username and password and try again.",
        )
        return response