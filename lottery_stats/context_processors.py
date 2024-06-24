from django.contrib.auth.models import User
from orders.models import Subscription


def subscription_access(request):
    """
    Determines the access levels for various subscriptions based on the user's
    authentication status.

    This function checks if the user is authenticated and, if so, queries the
    Subscription model to check for active subscriptions that grant access to
    specific services. It returns a dictionary indicating whether the user has
    access to AI Predictions, Premium services, and Statistics.

    Args:
        request (HttpRequest): The HttpRequest object containing metadata
        about the request.

    Returns:
        dict: A dictionary with boolean values that indicate whether the user
        has access to:
            - AI Predictions (has_ai_access)
            - Premium Full Access (has_premium_access)
            - Lotto Statistics (has_statistics_access)

    The function ensures that if the user is not authenticated, all access
    permissions are set to False, reinforcing security by denying access to
    critical features based on subscription status.
    """
    if request.user.is_authenticated:
        user_subscriptions = Subscription.objects.filter(
            user=request.user, active=True
        )
        has_ai_access = user_subscriptions.filter(
            product_name="AI Predictions for EuroMillions Lotto"
        ).exists()
        has_premium_access = user_subscriptions.filter(
            product_name="Premium Full Access"
        ).exists()
        has_statistics_access = user_subscriptions.filter(
            product_name="Lotto Statistics for EuroMillions"
        ).exists()
    else:
        has_ai_access = has_premium_access = has_statistics_access = False

    return {
        "has_ai_access": has_ai_access,
        "has_premium_access": has_premium_access,
        "has_statistics_access": has_statistics_access,
    }