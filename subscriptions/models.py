from django.db import models
from django.contrib.auth.models import User

class Subscription(models.Model):
    # One-to-one relationship with the User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    # Subscription stats fields
    subscribe_stats = models.CharField(max_length=3, choices=[('YES', 'Yes'), ('NO', 'No')])
    subscribe_stats_date = models.DateField(blank=True, null=True)
    subscribe_stats_date_expiry = models.DateField(blank=True, null=True)
    subscribe_stats_cancel_date = models.DateField(blank=True, null=True)

    # Subscription predictions fields
    subscribe_predictions = models.CharField(max_length=3, choices=[('YES', 'Yes'), ('NO', 'No')])
    subscribe_predictions_date = models.DateField(blank=True, null=True)
    subscribe_predictions_date_expiry = models.DateField(blank=True, null=True)
    subscribe_predictions_cancel_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username  # Using the related User object's username as the string representation
