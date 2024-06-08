from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from django.contrib import messages
from orders.models import Subscription

@login_required
def profile_view(request):
    user = request.user
    email = EmailAddress.objects.get(user=user)
    subscriptions = Subscription.objects.filter(user=user)
    return render(request, 'user_profile/profile.html', {'user': user, 'email': email, 'subscriptions': subscriptions})


@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST['username']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.save()
        
        email = EmailAddress.objects.get(user=user)
        email.email = request.POST['email']
        email.save()
        
        messages.success(request, 'Your profile was updated successfully.')
        return render(request, 'user_profile/profile.html', {'user': user, 'email': email})
    else:
        return render(request, 'user_profile/profile.html', {'user': request.user, 'email': EmailAddress.objects.get(user=request.user)})

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
