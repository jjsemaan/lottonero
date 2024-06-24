from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from djstripe.settings import djstripe_settings
from orders.models import Subscription as OrdersSubscription
from djstripe.models import (
    Subscription as DJStripeSubscription,
    Product,
    Price,
)
from .models import Subscription
from django.core.mail import send_mail, EmailMessage
from django.db.models import Sum
from predictions.models import Prediction, ShuffledPrediction
import stripe


@login_required
def pricing_page(request):
    """
    Renders the pricing page with available subscription options and their
    statuses.

    This view checks the user's current subscription statuses to determine
    which subscription options to display as available or already subscribed.
    It provides detailed information about different subscription packages,
    utilizing Stripe API keys for payment processing if needed. The page also
    displays placeholder information for total wins and the latest jackpot
    result.

    Args:
        request (HttpRequest): The HTTP request object containing metadata
        about the request.

    Returns:
        HttpResponse: An HttpResponse object that renders the pricing_page.html
        template with the context containing various settings and status flags
        related to subscription options and other relevant user-specific data.

    The function checks if the user already has active subscriptions such as
    'AI Predictions for EuroMillions Lotto', 'Premium Full Access', and
    'Lotto Statistics for EuroMillions'. It then adjusts the display options
    accordingly to inform the user of available or subscribed services.
    """
    user_subscriptions = Subscription.objects.filter(
        user=request.user, active=True
    )
    has_ai = user_subscriptions.filter(
        product_name="AI Predictions for EuroMillions Lotto"
    ).exists()
    has_premium = user_subscriptions.filter(
        product_name="Premium Full Access"
    ).exists()
    has_statistics = user_subscriptions.filter(
        product_name="Lotto Statistics for EuroMillions"
    ).exists()
    display_premium = not has_premium and (not has_statistics and not has_ai)
    display_ai = not has_premium and not has_ai
    display_statistics = not has_premium and not has_statistics

    context = {
        "stripe_public_key": settings.STRIPE_TEST_PUBLIC_KEY,
        "predictions_stripe_pricing_table_id": settings.PREDICTIONS_STRIPE_PRICING_TABLE_ID,
        "premium_stripe_pricing_table_id": settings.PREMIUM_STRIPE_PRICING_TABLE_ID,
        "statistics_stripe_pricing_table_id": settings.STATISTICS_STRIPE_PRICING_TABLE_ID,
        "has_ai": has_ai,
        "has_premium": has_premium,
        "has_statistics": has_statistics,
        "total_wins_till_date": "Get your data here",
        "latest_result": {"jackpot": "Latest Jackpot Value"},
        "display_premium": display_premium,
        "display_ai": display_ai,
        "display_statistics": display_statistics,
    }
    return render(request, "pricing_page/pricing_page.html", context)


@login_required
def subscription_confirm(request):
    """
    Handles the subscription confirmation process after a Stripe checkout
    session.

    This view retrieves the session ID from the request, confirms it with
    Stripe, and retrieves associated subscription data.
    It synchronizes subscription details with dj-stripe for local record
    keeping and updates product and price information. It also creates an
    order subscription record and sends a thank-you email to the user.

    Args:
        request (HttpRequest): The HttpRequest object containing metadata
        about the request including session details passed via GET parameters.

    Returns:
        HttpResponse: Renders a confirmation page if the subscription is
        successfully processed or returns an HttpResponseBadRequest if any step
        in the subscription confirmation fails due to invalid session, errors 
        in retrieving or syncing subscription data, or any other exception
        during processing.

    Uses:
        - Stripe API for retrieving checkout session and subscription data.
        - dj-stripe models for syncing subscription data locally.
        - Django's messaging framework for user notifications.
        - Django's email framework for sending a thank-you email.

    The function performs several key operations:
        - Validating and retrieving the Stripe session.
        - Fetching and validating the subscription from Stripe.
        - Syncing subscription and product details with dj-stripe.
        - Creating a local order subscription record.
        - Sending a thank-you email to the user.

    Potential errors during the process are handled with detailed logging
    and user-friendly error messages.
    """
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
        djstripe_subscription = DJStripeSubscription.sync_from_stripe_data(
            subscription
        )
        print(f"Synced subscription: {djstripe_subscription}")
    except Exception as e:
        print(f"Error syncing subscription: {e}")
        return HttpResponseBadRequest("Error syncing subscription.")

    if djstripe_subscription:
        print("Subscription synced successfully with dj-stripe!")
    else:
        print("Subscription sync with dj-stripe failed!")

    try:
        for item in subscription["items"]["data"]:
            plan = item["plan"]
            price = item["price"]
            product = plan["product"]

            if isinstance(product, str):
                product = stripe.Product.retrieve(product)
            djstripe_product = Product.sync_from_stripe_data(product)

            if isinstance(price, str):
                price = stripe.Price.retrieve(price)
            djstripe_price = Price.sync_from_stripe_data(price)

            if djstripe_product.default_price != djstripe_price:
                djstripe_product.default_price = djstripe_price
                djstripe_product.save()

            print(
                f"Product and price synced successfully for product: {product}"
            )

        product_name = (
            djstripe_product.name if djstripe_product else "Unknown Product"
        )

        OrdersSubscription.objects.create(
            user=request.user,
            email=request.user.email,
            prod_id=plan["product"],
            product_name=product_name,
            active=plan["active"],
            interval=plan["interval"],
            cust_id=subscription["customer"],
            invoice_id=subscription["latest_invoice"],
            subscription_id=subscription["id"],
        )

        print("OrdersSubscription created successfully!")

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
            html_message=message,
        )

        print("Email sent successfully!")

    except Exception as e:
        print(f"Error syncing product and price: {e}")
        return HttpResponseBadRequest("Error syncing product and price.")

    messages.success(
        request, "You've successfully signed up. Thanks for the support!"
    )

    return render(
        request,
        "subscription_confirm/subscription_confirm.html",
        {"subscription": djstripe_subscription},
    )


@login_required
def cancel_subscription_view(request, subscription_id):
    """
    Processes subscription cancellation requests and sends a confirmation
    email to the user.

    This view retrieves the specified subscription by its ID, ensuring it
    belongs to the current user. If the user confirms cancellation via a POST
    request, the subscription is cancelled, a success message is displayed,
    and a confirmation email is sent. If the request is not a POST or the user
    has not confirmed cancellation, it renders a confirmation page.

    Args:
        request (HttpRequest): The HttpRequest object containing metadata
        about the request.
        subscription_id (int): The ID of the subscription to cancel.

    Returns:
        HttpResponse: If POST and cancellation confirmed, redirects to the
        user profile page. Otherwise, renders a confirmation page to confirm
        the action before proceeding.

    This function handles the following:
    - User authentication and authorization to cancel the specified
    subscription.
    - Sending a detailed cancellation confirmation email to the user
    upon successful cancellation.
    - Redirecting to the profile view on successful cancellation or
    rendering a confirmation view otherwise.
    """
    subscription = get_object_or_404(
        Subscription, id=subscription_id, user=request.user
    )

    if request.method == "POST":
        if "confirm_cancel" in request.POST:
            subscription.cancel_subscription()
            messages.success(
                request, "Your subscription has been successfully cancelled."
            )

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
            bcc = ["admin@lottonero.com"]

            email = EmailMessage(
                subject, html_content, from_email, recipient_list, bcc=bcc
            )
            email.content_subtype = "html"
            email.send(fail_silently=False)

            return redirect("user_profile:profile_view")

    context = {"subscription": subscription}
    return render(request, "confirm_cancel/confirm_cancel.html", context)
