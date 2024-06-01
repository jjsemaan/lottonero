from django.shortcuts import render, redirect
from .models import Subscription, SubscriptionType

def subscription_types_view(request):
    """
    View to display all subscription types as banners.
    """
    subscription_types = SubscriptionType.objects.all()
    context = {
        'subscription_types': subscription_types,
    }
    return render(request, 'plans/plans.html', context)


from django.contrib.auth.decorators import login_required
from .forms import OrderForm

@login_required
def checkout(request, subscription_id):
    subscription_type = SubscriptionType.objects.get(id=subscription_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, user=request.user, subscription_type=subscription_type)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.user = request.user
            subscription.subscription_type = subscription_type
            subscription.subscribe_price = form.cleaned_data['total_price']
            subscription.total_price = form.cleaned_data['total_price']
            subscription.save()
            return redirect('subscription_success')  # Redirect to a success page
    else:
        form = OrderForm(user=request.user, subscription_type=subscription_type)

    context = {
        'form': form,
        'subscription_type': subscription_type,
    }
    return render(request, 'checkout/checkout.html', context)

def subscription_success(request):
    return render(request, 'checkout/subscription_success.html')
