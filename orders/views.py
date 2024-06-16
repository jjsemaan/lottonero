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


from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from djstripe.settings import djstripe_settings

@login_required
def pricing_page(request):
    context = {
        'stripe_public_key': settings.STRIPE_PUBLISHABLE_KEY,
        'stripe_pricing_table_id': settings.STRIPE_PRICING_TABLE_ID,
    }
    return render(request, 'pricing_page/pricing_page.html', context)
    

from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from djstripe.settings import djstripe_settings
from djstripe.models import Subscription, Product, Price
import stripe

@login_required
def subscription_confirm(request):
    # Set up Stripe keys
    stripe.api_key = djstripe_settings.STRIPE_SECRET_KEY

    # Get the session id from the URL and retrieve the session object from Stripe
    session_id = request.GET.get("session_id")
    if not session_id:
        return HttpResponseBadRequest("No session ID provided.")

    try:
        session = stripe.checkout.Session.retrieve(session_id)
    except stripe.error.InvalidRequestError:
        return HttpResponseBadRequest("Invalid session ID.")

    # Get the subscribing user from the client_reference_id we passed in above
    client_reference_id = int(session.client_reference_id)
    subscription_holder = get_user_model().objects.get(id=client_reference_id)
    # Sanity check that the logged-in user is the one being updated
    assert subscription_holder == request.user

    # Get the subscription object from Stripe and sync to djstripe
    subscription = stripe.Subscription.retrieve(session.subscription)
    djstripe_subscription = Subscription.sync_from_stripe_data(subscription)

    # Ensure the product and price are correctly synced
    for item in subscription.items.data:
        plan = item.plan
        product = plan.product
        price = plan

        # Retrieve and sync product and price
        if isinstance(product, str):
            product = stripe.Product.retrieve(product)
        if isinstance(price, str):
            price = stripe.Price.retrieve(price)

        djstripe_product = Product.sync_from_stripe_data(product)
        djstripe_price = Price.sync_from_stripe_data(price)

        # Check if the default price needs to be updated
        if djstripe_product.default_price != djstripe_price:
            djstripe_product.default_price = djstripe_price
            djstripe_product.save()

    # Show a message to the user
    messages.success(request, "You've successfully signed up. Thanks for the support!")
    
    # Render the confirmation template
    return render(request, 'subscription_confirm.html', {'subscription': djstripe_subscription})
