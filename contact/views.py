from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ContactMessageForm

@login_required
def contact_view(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            contact_message = form.save(commit=False)
            contact_message.user = request.user
            contact_message.save()
            return render(request, 'contact/thank_you.html')
    else:
        form = ContactMessageForm()
    return render(request, 'contact/contact_form.html', {'form': form})
