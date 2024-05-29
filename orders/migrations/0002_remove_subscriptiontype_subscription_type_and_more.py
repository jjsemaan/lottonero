# Generated by Django 4.2.11 on 2024-05-29 19:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscriptiontype',
            name='subscription_type',
        ),
        migrations.AddField(
            model_name='subscriptiontype',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscriptiontype',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='subscriptiontype',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
