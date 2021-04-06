# Generated by Django 3.1.7 on 2021-03-05 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_app', '0002_auto_20210305_1513'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee_profile',
            name='date_of_birth',
        ),
        migrations.AddField(
            model_name='employee_profile',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]