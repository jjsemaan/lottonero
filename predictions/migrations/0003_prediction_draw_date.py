# Generated by Django 4.2.11 on 2024-05-24 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0002_prediction_match_type_prediction_winning_balls_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='prediction',
            name='draw_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]