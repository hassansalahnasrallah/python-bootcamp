# Generated by Django 3.1.7 on 2021-03-21 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_app', '0024_auto_20210318_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
