from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from django.contrib import messages
from orders.models import Subscription

@login_required
def profile_view(request):
    user = request.user
    primary_email = EmailAddress.objects.filter(user=user, primary=True).first()  # Retrieve the primary email
    subscriptions = Subscription.objects.filter(user=user)
    return render(request, 'user_profile/profile.html', {
        'user': user,
        'primary_email': primary_email,  # Pass the primary email to the template
        'subscriptions': subscriptions
    })

@login_required
def update_profile(request):
    user = request.user
    primary_email = EmailAddress.objects.filter(user=user, primary=True).first()
    subscriptions = Subscription.objects.filter(user=user)  # Fetch subscriptions for both POST and GET

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)

        # Update username if your policy allows it
        username = request.POST.get('username', user.username)
        user.username = username  # Make sure to handle unique constraint

        user.save()

        messages.success(request, 'Your profile was updated successfully.')
        render(request, 'user_profile/profile.html')  # Redirect to a profile view page to avoid double submission

    # Display the profile edit page
    return render(request, 'user_profile/profile.html', {
        'user': user,
        'primary_email': primary_email,
        'subscriptions': subscriptions
    })

@login_required
def change_password(request):
    if request.method == 'POST':
        user = request.user
        new_password = request.POST['new_password']
        user.set_password(new_password)
        user.save()
        messages.success(request, 'Your password was changed successfully.')
        return render(request, 'user_profile/profile.html', {'user': user, 'email': EmailAddress.objects.get(user=user)})
    else:
        return render(request, 'user_profile/change_password.html')


def terms_and_conditions(request):
    return render(request, 'terms_and_conditions/terms_and_conditions.html')

