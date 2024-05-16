from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

class SubscriptionType(models.Model):
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
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    subscription_type = models.ForeignKey(SubscriptionType, on_delete=models.SET_NULL, null=True, blank=True)
    subscribe_end_date = models.DateField(blank=True, null=True)
    subscribe_cancel_date = models.DateField(blank=True, null=True)
    subscribe_renewal_date = models.DateField(blank=True, null=True)
    subscribe_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.subscribe_end_date:
            self.subscribe_end_date = self.created_on.date() + timedelta(days=365)
        if not self.subscribe_renewal_date:
            self.subscribe_renewal_date = self.created_on.date() + timedelta(days=365)
        if self.subscription_type and not self.subscribe_price:
            self.subscribe_price = self.subscription_type.price
        super(Subscription, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} ({self.user.email})"
