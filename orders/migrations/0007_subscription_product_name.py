# Generated by Django 4.2.11 on 2024-06-20 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_remove_subscription_event_id_subscription_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='product_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
