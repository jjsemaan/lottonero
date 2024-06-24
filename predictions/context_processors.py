from django.contrib.auth.models import User
from orders.models import Subscription
from django.db.models import Sum, Q
from predictions.models import Prediction, ShuffledPrediction


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

def total_winning_amount(request):
    """
    Calculate the combined total winning amount from both Prediction and ShuffledPrediction models.

    This context processor aggregates the total winnings from the 'win_amount' fields of Prediction
    and ShuffledPrediction models, where winnings are greater than zero and not null. It is designed
    to be used to globally provide the combined winning total to all templates rendered within the
    Django project.

    Args:
        request (HttpRequest): The HTTP request object, which is not directly used in this function
        but is necessary for context processors in Django.

    Returns:
        dict: A dictionary containing 'total_combined_winning_amount' as a key with the aggregated
        total winnings as its value. This allows the total winnings to be accessible as a context
        variable in all templates.
    """
    total_win_amount_predictions = Prediction.objects.filter(
        win_amount__isnull=False, win_amount__gt=0
    ).aggregate(total=Sum('win_amount'))['total'] or 0

    total_win_amount_shuffled = ShuffledPrediction.objects.filter(
        win_amount__isnull=False, win_amount__gt=0
    ).aggregate(total=Sum('win_amount'))['total'] or 0

    total_combined_winning_amount = total_win_amount_predictions + total_win_amount_shuffled

    return {'total_combined_winning_amount': total_combined_winning_amount}

