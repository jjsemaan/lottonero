# Generated by Django 3.2.25 on 2024-05-01 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LotteryResult',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('draw_date', models.CharField(help_text='Date of the EuroMillions draw.', max_length=100)),
                ('ball_1', models.IntegerField(help_text='First ball drawn.')),
                ('ball_2', models.IntegerField(help_text='Second ball drawn.')),
                ('ball_3', models.IntegerField(help_text='Third ball drawn.')),
                ('ball_4', models.IntegerField(help_text='Fourth ball drawn.')),
                ('ball_5', models.IntegerField(help_text='Fifth ball drawn.')),
                ('lucky_ball_1', models.IntegerField(help_text='First Lucky Star ball.')),
                ('lucky_ball_2', models.IntegerField(help_text='Second Lucky Star ball.')),
            ],
            options={
                'db_table': 'lottonero_balls',
            },
        ),
    ]
