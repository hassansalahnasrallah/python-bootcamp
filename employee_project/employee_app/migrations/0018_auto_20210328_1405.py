# Generated by Django 3.1.7 on 2021-03-28 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_app', '0017_auto_20210322_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee_vacation',
            name='Duration',
            field=models.IntegerField(),
        ),
    ]
