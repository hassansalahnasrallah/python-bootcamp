# Generated by Django 3.1.7 on 2021-03-03 13:39

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employee_app', '0002_auto_20210303_1530'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserSignup',
            new_name='UserProfile',
        ),
    ]
