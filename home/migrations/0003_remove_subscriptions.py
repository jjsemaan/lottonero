# home/migrations/000X_remove_subscriptions.py

from django.db import migrations

def drop_subscriptions_tables(apps, schema_editor):
    schema_editor.execute("DROP TABLE IF EXISTS subscriptions_subscription;")

class Migration(migrations.Migration):

    dependencies = [
        # Add the last migration file of the 'home' app here
        ('home', '0002_delete_lotteryresult'),
    ]

    operations = [
        migrations.RunPython(drop_subscriptions_tables),
    ]
