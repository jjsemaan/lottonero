from django.contrib.auth.models import User
from orders.models import Subscription

def subscription_access(request):
    if request.user.is_authenticated:
        user_subscriptions = Subscription.objects.filter(user=request.user, active=True)
        has_ai_access = user_subscriptions.filter(product_name="AI Predictions for EuroMillions Lotto").exists()
        has_premium_access = user_subscriptions.filter(product_name="Premium Full Access").exists()
        has_statistics_access = user_subscriptions.filter(product_name="Lotto Statistics for EuroMillions").exists()
    else:
        has_ai_access = has_premium_access = has_statistics_access = False

    return {
        'has_ai_access': has_ai_access,
        'has_premium_access': has_premium_access,
        'has_statistics_access': has_statistics_access,
    }
