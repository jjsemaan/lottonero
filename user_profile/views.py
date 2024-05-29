from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from django.contrib import messages

@login_required
def profile_view(request):
    user = request.user
    email = EmailAddress.objects.get(user=user)
    return render(request, 'user_profile/profile.html', {'user': user, 'email': email})

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
        return redirect('profile_view')
    else:
        return redirect('profile_view')

@login_required
def change_password(request):
    if request.method == 'POST':
        user = request.user
        new_password = request.POST['new_password']
        user.set_password(new_password)
        user.save()
        messages.success(request, 'Your password was changed successfully.')
        return redirect('profile_view')
    else:
        return render(request, 'user_profile/change_password.html')
