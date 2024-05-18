from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django_summernote.fields import SummernoteTextField

class SubscriptionType(models.Model):
    """
    Model representing a subscription type (subscription plans). Each subscription type has an id,
    name, description, and price.

    Attributes:
        subscription_type (str): The code for the subscription type (e.g., 'STA' for Statistics).
        name (str): The name of the subscription type.
        description (str): A detailed description of the subscription type.
        price (Decimal): The price of the subscription.
    """
    STATISTICS = 'STA'
    PREDICTIONS = 'PRE'
    FULL_SUBSCRIPTION = 'FUL'
    SELECT = 'SEL'
    SUBSCRIBE_TYPE_CHOICES = [
        (STATISTICS, 'Statistics'),
        (PREDICTIONS, 'Predictions'),
        (FULL_SUBSCRIPTION, 'Full Subscription'),
        (SELECT, 'Select'),
    ]

    subscription_type = models.CharField(max_length=3, choices=SUBSCRIBE_TYPE_CHOICES, unique=True)
    name = models.CharField(max_length=100)
    description = SummernoteTextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        """
        Returns a string representation of the subscription type, which is its name.
        """
        return self.name

class Subscription(models.Model):
    """
    Model representing a user's subscription. Each subscription is linked to a user and a subscription type.

    Attributes:
        user (User): The user who owns the subscription.
        subscription_type (SubscriptionType): The type of subscription.
        subscribe_end_date (date): The date when the subscription ends.
        subscribe_cancel_date (date): The date when the subscription was canceled.
        subscribe_renewal_date (date): The date when the subscription will be renewed.
        subscribe_price (Decimal): The price of the subscription.
        created_on (datetime): The date and time when the subscription was created.
        total_price (Decimal): The total price paid for the subscription.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    subscription_type = models.ForeignKey(SubscriptionType, on_delete=models.SET_NULL, null=True, blank=True)
    subscribe_end_date = models.DateField(blank=True, null=True)
    subscribe_cancel_date = models.DateField(blank=True, null=True)
    subscribe_renewal_date = models.DateField(blank=True, null=True)
    subscribe_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to automatically set the subscribe_end_date and subscribe_renewal_date
        to 12 months from the created_on date if they are not already set. It also sets the subscribe_price
        based on the subscription_type if not already set.
        """
        if not self.subscribe_end_date:
            self.subscribe_end_date = self.created_on.date() + timedelta(days=365)
        if not self.subscribe_renewal_date:
            self.subscribe_renewal_date = self.created_on.date() + timedelta(days=365)
        if self.subscription_type and not self.subscribe_price:
            self.subscribe_price = self.subscription_type.price
        super(Subscription, self).save(*args, **kwargs)

    def __str__(self):
        """
        Returns a string representation of the subscription, which includes the username and email of the user.
        """
        return f"{self.user.username} ({self.user.email})"
