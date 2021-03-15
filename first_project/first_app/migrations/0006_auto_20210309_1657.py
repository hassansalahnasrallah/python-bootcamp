# Generated by Django 3.1.7 on 2021-03-09 14:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('first_app', '0005_auto_20210309_1531'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profilepagemodel',
            name='id',
        ),
        migrations.AlterField(
            model_name='profilepagemodel',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
