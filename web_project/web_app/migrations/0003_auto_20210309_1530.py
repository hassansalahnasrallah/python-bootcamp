# Generated by Django 3.1.7 on 2021-03-09 13:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web_app', '0002_auto_20210309_0237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
    ]