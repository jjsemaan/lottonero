from django.apps import AppConfig


class LotteryStatsConfig(AppConfig):
    """
    AppConfig subclass for the 'LotteryStats' application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lottery_stats'
