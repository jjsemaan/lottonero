from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import (
    AuthenticatedContactMessageForm,
    UnauthenticatedContactMessageForm,
)
from .models import ContactMessage


def contact_view(request):
    """
    Handles the contact page requests for both authenticated and unauthenticated users.

    This view manages the submission of contact forms. For authenticated users, it pre-fills and
    submits the form using their stored information. For unauthenticated users, it requires manual
    entry of contact details. After form validation, it saves the contact message to the database
    and sends an email notification to the site administrator.

    For POST requests:
        - Uses `AuthenticatedContactMessageForm` if the user is logged in, pre-filling the user's
          details into the form and associating the message with the user's account.
        - Uses `UnauthenticatedContactMessageForm` for visitors without an account, requiring
          manual input of contact information.
        - Upon form validation, saves the message and sends an email with the message content.
        - Redirects to a 'thank you' page upon successful submission.

    For GET requests:
        - Provides a blank form for the user to fill out, choosing the form type based on
          authentication status.

    Args:
        request (HttpRequest): The request object used to access various metadata of the incoming HTTP request.

    Returns:
        HttpResponse: Renders the contact form or redirects to the thank-you page upon successful form submission.

    Template used:
        - 'contact/contact_form.html' for displaying the form.
        - 'contact/thank_you.html' for displaying the thank you page upon successful submission.
    """
    if request.method == "POST":
        if request.user.is_authenticated:
            form = AuthenticatedContactMessageForm(request.POST)
            if form.is_valid():
                contact_message = form.save(commit=False)
                contact_message.user = request.user
                contact_message.full_name = (
                    f"{request.user.first_name} {request.user.last_name}"
                )
                contact_message.email = request.user.email
                contact_message.save()

                # Send email
                send_mail(
                    subject=f"New message from {request.user.email}",
                    message=contact_message.message,
                    from_email="donotreply@lottonero.com",
                    recipient_list=["admin@lottonero.com"],
                    fail_silently=False,
                )

                return render(request, "contact/thank_you.html")
        else:
            form = UnauthenticatedContactMessageForm(
                request.POST, user=request.user
            )
            if form.is_valid():
                contact_message = form.save()

                # Send email
                send_mail(
                    subject=f"New message from {form.cleaned_data['email']}",
                    message=contact_message.message,
                    from_email="donotreply@lottonero.com",
                    recipient_list=["admin@lottonero.com"],
                    fail_silently=False,
                )

                return render(request, "contact/thank_you.html")
    else:
        if request.user.is_authenticated:
            form = AuthenticatedContactMessageForm()
        else:
            form = UnauthenticatedContactMessageForm(user=request.user)

    context = {
        "form": form,
        "user": request.user if request.user.is_authenticated else None,
    }
    return render(request, "contact/contact_form.html", context)

def about(request):
    return render(request, "about/about.html")

