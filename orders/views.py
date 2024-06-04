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
from decimal import Decimal
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def checkout(request, subscription_id):
    subscription_type = SubscriptionType.objects.get(id=subscription_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, user=request.user, subscription_type=subscription_type)
        if form.is_valid():
            if not request.user.first_name:
                request.user.first_name = form.cleaned_data['first_name']
            if not request.user.last_name:
                request.user.last_name = form.cleaned_data['last_name']
            request.user.save()
            
            subscription_option = form.cleaned_data['subscription_option']
            monthly_price = subscription_type.price
            annual_price = (monthly_price * Decimal(12) * Decimal(0.85)).quantize(Decimal('0.01'))
            subscribe_price = monthly_price if subscription_option == 'monthly' else annual_price
            
            subscription = Subscription(
                user=request.user,
                subscription_type=subscription_type,
                subscribe_price=subscribe_price,
                total_price=subscribe_price,
                subscribe_end_date=datetime.now().date() + timedelta(days=365),
                subscribe_cancel_date=request.POST.get('subscribe_cancel_date'),
                subscribe_renewal_date=datetime.now().date() + timedelta(days=365),
                email=request.user.email,
            )
            subscription.save()
            return redirect('subscription_success')
    else:
        form = OrderForm(user=request.user, subscription_type=subscription_type)

    # Create a PaymentIntent
    intent = stripe.PaymentIntent.create(
        amount=int(subscription_type.price * 100),  # amount in cents
        currency='eur',
    )

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
        'stripe_public_key': settings.STRIPE_PUBLISHABLE_KEY,
        'client_secret': intent.client_secret,
    }
    return render(request, 'checkout/checkout.html', context)

def subscription_success(request):
    return render(request, 'checkout/subscription_success.html')


"""
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm
from django.conf import settings

def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': settings.STRIPE_PUBLISHABLE_KEY,
        'client_secret': settings.STRIPE_SECRET_KEY,
    }

    return render(request, template, context)
"""
