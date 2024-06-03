# Generated by Django 4.2.11 on 2024-06-03 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='subscription_start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='subscription_status',
            field=models.CharField(default='active', max_length=20),
        ),
        migrations.AddField(
            model_name='subscription',
            name='trial_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='recurring_subscription',
            field=models.BooleanField(default=True),
        ),
    ]
