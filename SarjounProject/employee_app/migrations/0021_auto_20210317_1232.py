# Generated by Django 3.1.7 on 2021-03-17 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_app', '0020_auto_20210317_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='dateofbirth',
            field=models.CharField(max_length=255),
        ),
    ]