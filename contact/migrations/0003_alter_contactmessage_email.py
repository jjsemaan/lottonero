# Generated by Django 4.2.11 on 2024-06-23 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "contact",
            "0002_contactmessage_email_contactmessage_full_name_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="contactmessage",
            name="email",
            field=models.EmailField(blank=True, max_length=40, null=True),
        ),
    ]
