from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from user_profile.models import UserProfile

class Command(BaseCommand):
    help = 'Import existing users into UserProfile'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            # Check if the user already has a UserProfile
            if not UserProfile.objects.filter(user=user).exists():
                # Create a UserProfile for the user
                UserProfile.objects.create(user=user)
                self.stdout.write(self.style.SUCCESS(f'Successfully created UserProfile for user {user.username}'))
            else:
                self.stdout.write(self.style.WARNING(f'UserProfile already exists for user {user.username}'))
