# Generated by Django 3.1.7 on 2021-03-17 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee_app', '0014_auto_20210317_1505'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee_profile',
            old_name='id1',
            new_name='id',
        ),
    ]