# Generated by Django 3.1.7 on 2021-03-15 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_app', '0012_vacation_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacation',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]