# Generated by Django 3.1.7 on 2021-03-22 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final_app', '0004_vacation_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacation',
            name='date_from',
            field=models.DateField(default=0),
        ),
        migrations.AddField(
            model_name='vacation',
            name='date_to',
            field=models.DateField(default=0),
        ),
    ]
