from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import AuthenticatedContactMessageForm, UnauthenticatedContactMessageForm
from .models import ContactMessage

def contact_view(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = AuthenticatedContactMessageForm(request.POST)
            if form.is_valid():
                contact_message = form.save(commit=False)
                contact_message.user = request.user
                contact_message.full_name = f"{request.user.first_name} {request.user.last_name}"
                contact_message.email = request.user.email
                contact_message.save()

                # Send email
                send_mail(
                    subject=f"New message from {request.user.email}",
                    message=contact_message.message,
                    from_email='donotreply@lottonero.com',
                    recipient_list=['admin@lottonero.com'],
                    fail_silently=False,
                )

                return render(request, 'contact/thank_you.html')
        else:
            form = UnauthenticatedContactMessageForm(request.POST, user=request.user)
            if form.is_valid():
                contact_message = form.save()

                # Send email
                send_mail(
                    subject=f"New message from {form.cleaned_data['email']}",
                    message=contact_message.message,
                    from_email='donotreply@lottonero.com',
                    recipient_list=['admin@lottonero.com'],
                    fail_silently=False,
                )

                return render(request, 'contact/thank_you.html')
    else:
        if request.user.is_authenticated:
            form = AuthenticatedContactMessageForm()
        else:
            form = UnauthenticatedContactMessageForm(user=request.user)

    context = {
        'form': form,
        'user': request.user if request.user.is_authenticated else None
    }
    return render(request, 'contact/contact_form.html', context)
