from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from django.contrib import messages
from orders.models import Subscription


@login_required
def profile_view(request):
    """
    Display the user's profile page including their primary email and subscription details.

    This view fetches the user's primary email address and their subscriptions to render the user profile page.
    It requires the user to be logged in.

    Args:
        request (HttpRequest): The HttpRequest object containing metadata about the request.

    Returns:
        HttpResponse: Renders the user_profile/profile.html template with the user's data including primary email
                      and subscriptions.
    """
    user = request.user
    primary_email = EmailAddress.objects.filter(
        user=user, primary=True
    ).first()
    subscriptions = Subscription.objects.filter(user=user)
    return render(
        request,
        "user_profile/profile.html",
        {
            "user": user,
            "primary_email": primary_email,
            "subscriptions": subscriptions,
        },
    )


@login_required
def update_profile(request):
    """
    Update the user's profile information such as name and username.

    This view allows users to update their first name, last name, and username. It handles POST requests with
    form data and saves the updated information to the user model. A success message is displayed after
    the update. It requires the user to be logged in.

    Args:
        request (HttpRequest): The HttpRequest object containing metadata about the request.

    Returns:
        HttpResponse: Renders the user_profile/profile.html template with updated user information or
                      re-renders the form in case of a GET request.
    """
    user = request.user
    primary_email = EmailAddress.objects.filter(
        user=user, primary=True
    ).first()
    subscriptions = Subscription.objects.filter(user=user)

    if request.method == "POST":
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)

        username = request.POST.get("username", user.username)
        user.username = username

        user.save()

        messages.success(request, "Your profile was updated successfully.")
        render(request, "user_profile/profile.html")

    return render(
        request,
        "user_profile/profile.html",
        {
            "user": user,
            "primary_email": primary_email,
            "subscriptions": subscriptions,
        },
    )


@login_required
def change_password(request):
    """
    Allows the user to change their password.

    This view processes POST requests where the user submits a new password. The user's password is updated
    in the database, and a success message is displayed. If accessed via GET, it presents the password change form.

    Args:
        request (HttpRequest): The HttpRequest object containing metadata about the request.

    Returns:
        HttpResponse: Redirects to the profile page on successful password change or renders the password
                      change form if accessed via GET.
    """
    if request.method == "POST":
        user = request.user
        new_password = request.POST["new_password"]
        user.set_password(new_password)
        user.save()
        messages.success(request, "Your password was changed successfully.")
        return render(
            request,
            "user_profile/profile.html",
            {"user": user, "email": EmailAddress.objects.get(user=user)},
        )
    else:
        return render(request, "user_profile/change_password.html")


def terms_and_conditions(request):
    return render(request, "terms_and_conditions/terms_and_conditions.html")


def privacy_policy(request):
    return render(request, "privacy_policy/privacy_policy.html")
