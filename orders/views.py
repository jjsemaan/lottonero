from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from djstripe.settings import djstripe_settings
from orders.models import Subscription as OrdersSubscription
from djstripe.models import Subscription as DJStripeSubscription, Product, Price
from .models import Subscription
from django.core.mail import send_mail, EmailMessage
import stripe

@login_required
def pricing_page(request):
    # Check if the current user has any active subscriptions
    user_subscriptions = Subscription.objects.filter(user=request.user, active=True)
    has_ai = user_subscriptions.filter(product_name="AI Predictions for EuroMillions Lotto").exists()
    has_premium = user_subscriptions.filter(product_name="Premium Full Access").exists()
    has_statistics = user_subscriptions.filter(product_name="Lotto Statistics for EuroMillions").exists()
    display_premium = not has_premium and (not has_statistics and not has_ai)
    display_ai = not has_premium and not has_ai
    display_statistics = not has_premium and not has_statistics

    context = {
        'stripe_public_key': settings.STRIPE_TEST_PUBLIC_KEY,
        'predictions_stripe_pricing_table_id': settings.PREDICTIONS_STRIPE_PRICING_TABLE_ID,
        'premium_stripe_pricing_table_id': settings.PREMIUM_STRIPE_PRICING_TABLE_ID,
        'statistics_stripe_pricing_table_id': settings.STATISTICS_STRIPE_PRICING_TABLE_ID,
        'has_ai': has_ai,
        'has_premium': has_premium,
        'has_statistics': has_statistics,
        'total_wins_till_date': "Get your data here",  # placeholder
        'latest_result': {'jackpot': "Latest Jackpot Value"},  # placeholder
        'display_premium': display_premium,
        'display_ai': display_ai,
        'display_statistics': display_statistics,
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
            user=request.user,  
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

        # Send a thank you email to the user
        user = request.user
        subject = "Thank you for your subscription!"
        message = f"""
        <html>
        <body>
            <p style="text-align:center;">Dear {user.first_name} {user.last_name},</p>
            <p style="text-align:center;">Thank you for your purchase!</p>
            <p style="text-align:center;">You have subscribed to "{product_name}". Your subscription is now active.</p>
            <p style="text-align:center;">However, if you are unable to access your subscription within two hours of this email, please contact us through the website.</p>
            <p style="text-align:center;">If at any point you decide to cancel your subscription, please visit your profile page.</p>
            <p style="text-align:center;">Sincerely,</p>
            <p style="text-align:center;">Lottonero Admin Team</p>
            <div style="text-align:center;">
                <a href="https://lottonero.com" style="display:inline-block;padding:10px 20px;font-size:16px;color:#ffffff;background-color:#007bff;border-radius:5px;text-align:center;text-decoration:none;">Visit Lottonero</a>
            </div>
        </body>
        </html>
        """
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]

        send_mail(
            subject,
            "Your Lottonero Subscription",
            from_email,
            recipient_list,
            fail_silently=False,
            html_message=message
        )

        print("Email sent successfully!")

    except Exception as e:
        print(f"Error syncing product and price: {e}")
        return HttpResponseBadRequest("Error syncing product and price.")

    # Show a message to the user
    messages.success(request, "You've successfully signed up. Thanks for the support!")
    
    # Render the confirmation template
    return render(request, 'subscription_confirm/subscription_confirm.html', {'subscription': djstripe_subscription})


@login_required
def cancel_subscription_view(request, subscription_id):
    subscription = get_object_or_404(Subscription, id=subscription_id, user=request.user)

    if request.method == 'POST':
        if 'confirm_cancel' in request.POST:
            subscription.cancel_subscription()
            messages.success(request, "Your subscription has been successfully cancelled.")

            # Prepare the email message
            subject = "Subscription Cancelled!"
            html_content = f"""
            <html>
            <body>
                <p style="text-align:center;">Dear {request.user.first_name} {request.user.last_name},</p>
                
                <p style="text-align:center;">Your subscription "{subscription.product_name}" has been cancelled.</p>
                <p style="text-align:center;">This might take five working days to complete. </p>
                <p style="text-align:center;">If at any point you decide to resubscribe, please visit us again.</p>
                <p style="text-align:center;">Sincerely,</p>
                <p style="text-align:center;">Lottonero Admin Team</p>
                <div style="text-align:center;">
                    <a href="https://lottonero.com" style="display:inline-block;padding:10px 20px;font-size:16px;color:#ffffff;background-color:#007bff;border-radius:5px;text-align:center;text-decoration:none;">Visit Lottonero</a>
                </div>
            </body>
            </html>
            """
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [request.user.email]
            bcc = ['admin@lottonero.com']

            # Create EmailMessage object
            email = EmailMessage(
                subject,
                html_content,
                from_email,
                recipient_list,
                bcc=bcc
            )
            email.content_subtype = "html"  # Specify the subtype as HTML
            email.send(fail_silently=False)

            return redirect('user_profile:profile_view')  # Assuming this is correctly named and namespaced

    # If it's not a POST request or no confirmation, show the confirmation page
    context = {
        'subscription': subscription
    }
    return render(request, 'confirm_cancel/confirm_cancel.html', context)


