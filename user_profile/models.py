from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from orders.models import Subscription, SubscriptionType

class UserProfile(models.Model):
    """
    Model representing a user profile. Each profile is linked to a user and optionally to a subscription type.

    Attributes:
        user (User): The user who owns the profile.
        subscription_type (SubscriptionType): The type of subscription associated with the profile, if any.
    
    Methods:
        __str__(): Returns a string representation of the profile, which is the username of the user.
        is_subscriber(): Checks if the user is currently a subscriber by verifying the presence of an active subscription.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription_type = models.ForeignKey(SubscriptionType, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        """
        Returns a string representation of the profile, which is the username of the user.
        """
        return self.user.username

    @property
    def is_subscriber(self):
        """
        Checks if the user is currently a subscriber.

        A user is considered a subscriber if they have a subscription with a subscribe_end_date
        that is in the future or today.

        Returns:
            bool: True if the user is a subscriber, False otherwise.
        """
        current_subscription = Subscription.objects.filter(
            user=self.user, subscribe_end_date__gte=timezone.now()
        ).exists()
        return current_subscription


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
