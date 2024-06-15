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
    stripe_public_key = settings.STRIPE_PUBLISHABLE_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

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
        amount=int(subscription_type.price * 100),
        currency='eur',
    )

    template = 'checkout/checkout.html'
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
    return render(request, template, context)

@login_required
def subscription_success(request):
    return render(request, 'checkout/subscription_success.html')


from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def subscription_confirm(request):
    return render(request, 'subscription_confirm.html')


from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from djstripe.settings import djstripe_settings


@login_required
def pricing_page(request):
    return render(request, 'pricing_page.html', {
        'stripe_public_key': djstripe_settings.STRIPE_PUBLIC_KEY,
        'stripe_pricing_table_id': settings.STRIPE_PRICING_TABLE_ID,
    })
    

# View to provision subscription
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from djstripe.settings import djstripe_settings
from djstripe.models import Subscription

import stripe

@login_required
def subscription_confirm(request):
    # set our stripe keys up
    stripe.api_key = djstripe_settings.STRIPE_SECRET_KEY

    # get the session id from the URL and retrieve the session object from Stripe
    session_id = request.GET.get("session_id")
    session = stripe.checkout.Session.retrieve(session_id)

    # get the subscribing user from the client_reference_id we passed in above
    client_reference_id = int(session.client_reference_id)
    subscription_holder = get_user_model().objects.get(id=client_reference_id)
    # sanity check that the logged in user is the one being updated
    assert subscription_holder == request.user

    # get the subscription object form Stripe and sync to djstripe
    subscription = stripe.Subscription.retrieve(session.subscription)
    djstripe_subscription = Subscription.sync_from_stripe_data(subscription)

    # set the subscription and customer on our user
    # subscription_holder.subscription = djstripe_subscription
    # subscription_holder.customer = djstripe_subscription.customer
    # subscription_holder.save()

    # show a message to the user and redirect
    messages.success(request, f"You've successfully signed up. Thanks for the support!")
    return HttpResponseRedirect(reverse("subscription_details"))
