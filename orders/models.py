from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from tinymce.models import HTMLField
import uuid

class SubscriptionType(models.Model):
    """
    Model representing a subscription type (subscription plans). Each subscription type has an id,
    name, description, price, created_on, and created_by.

    Attributes:
        name (str): The name of the subscription type.
        description (str): A detailed description of the subscription type.
        price (Decimal): The price of the subscription.
        created_on (datetime): The date and time when the subscription type was created.
        created_by (User): The user who created the subscription type.
    """
    name = models.CharField(max_length=100, unique=True)
    description = HTMLField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

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
        order_number (UUID): A unique identifier for the subscription.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    subscription_type = models.ForeignKey(SubscriptionType, on_delete=models.SET_NULL, null=True, blank=True)
    subscribe_end_date = models.DateField(blank=True, null=True)
    subscribe_cancel_date = models.DateField(blank=True, null=True)
    subscribe_renewal_date = models.DateField(blank=True, null=True)
    subscribe_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    order_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        if self.subscription_type:
            self.subscribe_price = self.subscription_type.price
        if not self.subscribe_end_date:
            self.subscribe_end_date = self.created_on.date() + timedelta(days=365)
        if not self.subscribe_renewal_date:
            self.subscribe_renewal_date = self.created_on.date() + timedelta(days=365)
        super(Subscription, self).save(*args, **kwargs)

    def __str__(self):
        """
        Returns a string representation of the subscription, which includes the username, email, and order number.
        """
        return f"{self.user.username} ({self.user.email}) - Order Number: {self.order_number}"