from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import datetime


class Profile(models.Model):
    """
    Extends User model to include additional user information.
    Fields include the user's location and phone number.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create or update the profile whenever a user
    instance is saved. Creates a new profile with the user
    instance if the user is created.
    """
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
