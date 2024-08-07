from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, datetime
from tinymce.models import HTMLField
import uuid


class Subscription(models.Model):
    """
    Model representing a user's subscription.

    Attributes:
        user (User): The user who owns the subscription.
        created_on (datetime): The date and time when the subscription was created.
        email (str): The email of the user, synced from the user's profile.
        active (bool): Indicates if the subscription is currently active.
        cancelled_on (datetime): The date and time when the subscription was cancelled.
        interval (str): The interval of the subscription (e.g., monthly, yearly).
        cust_id (str): The customer ID associated with the subscription.
        invoice_id (str): The invoice ID associated with the subscription.
        subscription_id (str): The subscription ID associated with the subscription.
        prod_id (str): The ID of the product associated with the subscription.
        product_name (str): The name of the product associated with the subscription.

    Methods:
        save(*args, **kwargs): Overrides the default save method to ensure the email
            is synced with the user's email before saving the subscription instance.
        cancel_subscription(): Cancels the subscription, setting it as inactive
            and recording the cancellation date.
        __str__(): Returns a string representation of the subscription instance,
            displaying the username, email, and product ID.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    active = models.BooleanField(default=True)
    interval = models.CharField(max_length=255, blank=True, null=True)
    cust_id = models.CharField(max_length=255, blank=True, null=True)
    invoice_id = models.CharField(max_length=255, blank=True, null=True)
    subscription_id = models.CharField(max_length=255, blank=True, null=True)
    prod_id = models.CharField(max_length=255, blank=True, null=True)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    cancelled_on = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Override the original save method to ensure email is synced with the user.
        """
        self.email = self.user.email
        super(Subscription, self).save(*args, **kwargs)

    def cancel_subscription(self):
        """
        Cancel the subscription and mark the cancellation time.
        """
        self.active = False
        self.cancelled_on = datetime.now()
        self.save()

    def __str__(self):
        return f"{self.user.username} ({self.email}) - Product ID: {self.prod_id} - Product Name: {self.product_name}"
