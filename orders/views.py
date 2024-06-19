from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.contrib.auth import get_user_model
from django.shortcuts import render
from djstripe.settings import djstripe_settings
from djstripe.models import Subscription, Product, Price
import stripe

@login_required
def pricing_page(request):
    """
    Renders the pricing page with the Stripe public key and pricing table ID.

    This view is protected by login_required, so only authenticated users can access it.

    Args:
        request (HttpRequest): The request object used to generate this response.

    Returns:
        HttpResponse: The rendered pricing page with context including Stripe public key 
                      and pricing table ID.
    """
    context = {
        'stripe_public_key': settings.STRIPE_TEST_PUBLIC_KEY,
        'stripe_pricing_table_id': settings.STRIPE_PRICING_TABLE_ID,
    }
    return render(request, 'pricing_page/pricing_page.html', context)

@login_required
def subscription_confirm(request):
    """
    Confirms a Stripe subscription and syncs it with dj-stripe.

    This view handles the following:
    1. Retrieves the session ID from the request.
    2. Retrieves the Stripe session and subscription objects.
    3. Syncs the subscription with the dj-stripe Subscription model.
    4. Ensures the associated products and prices are also synced with dj-stripe.
    5. Displays a success message to the user and renders the subscription confirmation page.

    Args:
        request (HttpRequest): The request object used to generate this response.

    Returns:
        HttpResponse: The rendered subscription confirmation page on success.
        HttpResponseBadRequest: If any errors occur during the process, such as missing 
                                session ID, invalid session ID, or issues with syncing data.
    """
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
    try:
        subscription = stripe.Subscription.retrieve(session.subscription)
        print(f"Retrieved subscription: {subscription}")
    except Exception as e:
        print(f"Error retrieving subscription: {e}")
        return HttpResponseBadRequest("Error retrieving subscription.")

    try:
        djstripe_subscription = Subscription.sync_from_stripe_data(subscription)
        print(f"Synced subscription: {djstripe_subscription}")
    except Exception as e:
        print(f"Error syncing subscription: {e}")
        return HttpResponseBadRequest("Error syncing subscription.")

    # Ensure the product and price are correctly synced
    try:
        for item in subscription['items']['data']:
            plan = item['plan']
            price = item['price']
            product = plan['product']

            # Retrieve and sync product
            if isinstance(product, str):
                product = stripe.Product.retrieve(product)
            djstripe_product = Product.sync_from_stripe_data(product)

            # Retrieve and sync price
            if isinstance(price, str):
                price = stripe.Price.retrieve(price)
            djstripe_price = Price.sync_from_stripe_data(price)

            # Check if the default price needs to be updated
            if djstripe_product.default_price != djstripe_price:
                djstripe_product.default_price = djstripe_price
                djstripe_product.save()

    except Exception as e:
        print(f"Error syncing product and price: {e}")
        return HttpResponseBadRequest("Error syncing product and price.")

    # Show a message to the user
    messages.success(request, "You've successfully signed up. Thanks for the support!")
    
    # Render the confirmation template
    return render(request, 'subscription_confirm/subscription_confirm.html', {'subscription': djstripe_subscription})
