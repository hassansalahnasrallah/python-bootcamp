# Generated by Django 3.1.7 on 2021-03-28 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_app', '0018_auto_20210328_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee_vacation',
            name='Duration',
            field=models.IntegerField(default=0),
        ),
    ]
