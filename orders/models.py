from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

class Subscription(models.Model):
    # One-to-one relationship with the User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    # Subscription types
    STATISTICS = 'STA'
    PREDICTIONS = 'PRE'
    FULL_SUBSCRIPTION = 'FUL'
    SELECT = 'SEL'
    SUBSCRIBE_TYPE_CHOICES = [
        (STATISTICS, 'Statistics'),
        (PREDICTIONS, 'Predictions'),
        (FULL_SUBSCRIPTION, 'Full Subscription'),
        (SELECT, 'Select'),  # Default value
    ]

    # Subscription fields
    subscribe_type = models.CharField(max_length=3, choices=SUBSCRIBE_TYPE_CHOICES, default=SELECT)
    subscribe_end_date = models.DateField(blank=True, null=True)  # Set to 12 months from created_on in save method
    subscribe_cancel_date = models.DateField(blank=True, null=True)
    subscribe_renewal_date = models.DateField(blank=True, null=True)  # Set to 12 months from created_on in save method
    subscribe_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Additional fields
    created_on = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Set subscribe_end_date and subscribe_renewal_date to 12 months from created_on if not already set
        if not self.subscribe_end_date:
            self.subscribe_end_date = self.created_on.date() + timedelta(days=365)
        if not self.subscribe_renewal_date:
            self.subscribe_renewal_date = self.created_on.date() + timedelta(days=365)
        super(Subscription, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} ({self.user.email})"  # Return both username and email
