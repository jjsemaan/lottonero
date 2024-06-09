# reset_subscriptions.py

from django.core.management.base import BaseCommand
from orders.models import Subscription
from django.db import connection

class Command(BaseCommand):
    help = 'Delete all records in orders_subscription and reset the primary key sequence'

    def handle(self, *args, **kwargs):
        self.stdout.write('Deleting all records from orders_subscription...')
        
        # Delete all records
        Subscription.objects.all().delete()
        
        # Reset primary key sequence
        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE orders_subscription_id_seq RESTART WITH 1;")
        
        self.stdout.write(self.style.SUCCESS('Successfully deleted all records and reset the primary key sequence.'))
