# Generated by Django 3.1.7 on 2021-03-14 09:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employee_app', '0005_auto_20210314_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee_vacation',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
