from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.contrib.auth import get_user_model
from django.shortcuts import render
from djstripe.settings import djstripe_settings
from orders.models import Subscription as OrdersSubscription
from djstripe.models import Subscription as DJStripeSubscription, Product, Price
from .models import Subscription
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
    stripe.api_key = djstripe_settings.STRIPE_SECRET_KEY

    session_id = request.GET.get("session_id")
    if not session_id:
        return HttpResponseBadRequest("No session ID provided.")

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        print(f"Retrieved session: {session}")
    except stripe.error.InvalidRequestError:
        return HttpResponseBadRequest("Invalid session ID.")

    if session:
        print("Session retrieved successfully!")
    else:
        print("Session retrieval failed!")

    try:
        subscription = stripe.Subscription.retrieve(session.subscription)
        print(f"Retrieved subscription: {subscription}")
    except Exception as e:
        print(f"Error retrieving subscription: {e}")
        return HttpResponseBadRequest("Error retrieving subscription.")

    if subscription:
        print("Subscription retrieved successfully!")
    else:
        print("Subscription retrieval failed!")

    try:
        djstripe_subscription = DJStripeSubscription.sync_from_stripe_data(subscription)
        print(f"Synced subscription: {djstripe_subscription}")
    except Exception as e:
        print(f"Error syncing subscription: {e}")
        return HttpResponseBadRequest("Error syncing subscription.")

    if djstripe_subscription:
        print("Subscription synced successfully with dj-stripe!")
    else:
        print("Subscription sync with dj-stripe failed!")

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

            print(f"Product and price synced successfully for product: {product}")

        # Retrieve the product name
        product_name = djstripe_product.name if djstripe_product else "Unknown Product"

        # Sync to OrdersSubscription model
        OrdersSubscription.objects.create(
            user=request.user,  # This is the foreign key to the User model
            email=request.user.email,
            prod_id=plan['product'],
            product_name=product_name,
            active=plan['active'],
            interval=plan['interval'],
            cust_id=subscription['customer'],
            invoice_id=subscription['latest_invoice'],
            subscription_id=subscription['id'],
        )

        print("OrdersSubscription created successfully!")

    except Exception as e:
        print(f"Error syncing product and price: {e}")
        return HttpResponseBadRequest("Error syncing product and price.")

    # Show a message to the user
    messages.success(request, "You've successfully signed up. Thanks for the support!")
    
    # Render the confirmation template
    return render(request, 'subscription_confirm/subscription_confirm.html', {'subscription': djstripe_subscription})
