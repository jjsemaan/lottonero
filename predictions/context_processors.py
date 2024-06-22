from django.contrib.auth.models import User
from orders.models import Subscription


def subscription_access(request):
    """
    Determines user's access to various subscription-based services.

    Checks if the authenticated user has active subscriptions and identifies the type of access they have,
    including access to AI predictions, premium features, and statistical data. If the user is not authenticated,
    all access rights are set to False.

    Args:
        request (HttpRequest): The HttpRequest object containing metadata about the request,
                               including the user's authentication status.

    Returns:
        dict: A dictionary indicating whether the user has access to AI predictions (`has_ai_access`),
              premium features (`has_premium_access`), and statistical data (`has_statistics_access`).
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
