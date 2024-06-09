# Generated by Django 4.2.11 on 2024-06-02 22:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', tinymce.models.HTMLField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscribe_end_date', models.DateField(blank=True, null=True)),
                ('subscribe_cancel_date', models.DateField(blank=True, null=True)),
                ('subscribe_renewal_date', models.DateField(blank=True, null=True)),
                ('subscribe_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('order_number', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('recurring_subscription', models.BooleanField(default=False)),
                ('subscription_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.subscriptiontype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]