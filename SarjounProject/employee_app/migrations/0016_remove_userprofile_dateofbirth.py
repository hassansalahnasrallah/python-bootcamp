# Generated by Django 3.1.7 on 2021-03-17 10:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee_app', '0015_auto_20210317_1210'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='dateofbirth',
        ),
    ]