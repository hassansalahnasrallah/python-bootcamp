# Generated by Django 3.1.7 on 2021-03-09 21:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finalapp', '0003_auto_20210307_1359'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vacationinfo',
            name='duration',
        ),
    ]
