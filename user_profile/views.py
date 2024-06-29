from django.shortcuts import redirect
from allauth.account.views import ConfirmEmailView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from django.contrib import messages
from orders.models import Subscription
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.conf import settings


@login_required
def profile_view(request):
    """
    Display the user's profile page including their primary email and
    subscription details.

    This view fetches the user's primary email address and their
    subscriptions to render the user profile page.
    It requires the user to be logged in.

    Args:
        request (HttpRequest): The HttpRequest object containing
        metadata about the request.

    Returns:
        HttpResponse: Renders the user_profile/profile.html template
        with the user's data including primary email
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

    This view allows users to update their first name, last name,
    and username. It handles POST requests with
    form data and saves the updated information to the user model.
    A success message is displayed after
    the update. It requires the user to be logged in.

    Args:
        request (HttpRequest): The HttpRequest object containing
        metadata about the request.

    Returns:
        HttpResponse: Renders the user_profile/profile.html template
        with updated user information or re-renders the form in case 
        of a GET request.
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
    Process a password change request for the logged-in user.

    Allows the user to submit a new password via a POST request.
    If the form data is valid, the user's password is updated and
    a success email is sent. A failure email is sent if the form
    validation fails. The user is redirected to the profile page
    on success and remains on the form with error messages if
    the update fails.

    Args:
        request (HttpRequest): The request object used to access
        session data and form data.

    Returns:
        HttpResponse: The HTTP response with either the redirection
        to the profile page on success or the password change form
        with error messages on failure.
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            # Send a success email notification
            send_mail(
                'Password Changed Successfully',
                'Your password has been successfully changed.',
                settings.DEFAULT_FROM_EMAIL,  # Use the default FROM email
                [user.email],
                fail_silently=False,
            )
            messages.success(request, 'Your password was changed successfully.')
            return render(request, "user_profile/profile.html")
        else:
            # Send an error email notification if password change fails
            send_mail(
                'Password Change Attempt Failed',
                'There was an attempt to change your password that did not meet the criteria.',
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=False,
            )
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'user_profile/change_password.html', {'form': form})

def terms_and_conditions(request):
    """
    A view that renders the terms and conditions page.
    """
    return render(request, "terms_and_conditions/terms_and_conditions.html")

def privacy_policy(request):
    """
    A view that renders the privacy policy page.
    """
    return render(request, "privacy_policy/privacy_policy.html")

class CustomConfirmEmailView(ConfirmEmailView):
    """
    Custom view to handle email confirmation and redirect
    to the account email page upon success.
    """
    def post(self, request, *args, **kwargs):
        """
        Handle the POST request to confirm the email and
        redirect to the account email page.
        """
        self.object = confirmation = self.get_object()
        confirmation.confirm(self.request)
        return redirect('account_email')
