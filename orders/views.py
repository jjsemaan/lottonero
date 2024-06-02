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


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Subscription, SubscriptionType
from .forms import OrderForm
from datetime import datetime, timedelta

@login_required
def checkout(request, subscription_id):
    subscription_type = SubscriptionType.objects.get(id=subscription_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, user=request.user, subscription_type=subscription_type)
        if form.is_valid():
            # Update user details if necessary
            if not request.user.first_name:
                request.user.first_name = form.cleaned_data['first_name']
            if not request.user.last_name:
                request.user.last_name = form.cleaned_data['last_name']
            request.user.save()
            
            subscription = Subscription(
                user=request.user,
                subscription_type=subscription_type,
                subscribe_price=subscription_type.price,
                total_price=form.cleaned_data['total_price'],
                subscribe_end_date=datetime.now().date() + timedelta(days=365),
                subscribe_cancel_date=request.POST.get('subscribe_cancel_date'),
                subscribe_renewal_date=datetime.now().date() + timedelta(days=365),
                email=request.user.email,
            )
            subscription.save()
            return redirect('subscription_success')  # Redirect to a success page
    else:
        form = OrderForm(user=request.user, subscription_type=subscription_type)

    context = {
        'form': form,
        'subscription_type': subscription_type,
        'user_info': {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        },
        'subscription_name': subscription_type.name,
        'subscription_description': subscription_type.description,
    }
    return render(request, 'checkout/checkout.html', context)

def subscription_success(request):
    return render(request, 'checkout/subscription_success.html')
