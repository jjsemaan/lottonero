from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, datetime
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


from django.db import models
from django.contrib.auth.models import User

class Subscription(models.Model):
    """
    Model representing a user's subscription.

    Attributes:
        user (User): The user who owns the subscription.
        created_on (datetime): The date and time when the subscription was created.
        email (str): The email of the user.
        active (bool): Indicates if the subscription is currently active.
        interval (str): The interval of the subscription (e.g., monthly, yearly).
        cust_id (str): The customer ID associated with the subscription.
        invoice_id (str): The invoice ID associated with the subscription.
        subscription_id (str): The subscription ID associated with the subscription.
        prod_id (str): The ID of the product associated with the subscription.

    Methods:
        save(*args, **kwargs): Overrides the default save method to ensure the email
            is synced with the user's email before saving the subscription instance.
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

    def save(self, *args, **kwargs):
        """
        Override the original save method to ensure email is synced with the user.
        """
        self.email = self.user.email
        super(Subscription, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} ({self.email}) - Product ID: {self.prod_id} - Product Name: {self.product_name}"

