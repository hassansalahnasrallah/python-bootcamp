# Generated by Django 3.1.7 on 2021-03-20 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finalapp', '0009_auto_20210318_2234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacationinfo',
            name='datefrom',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vacationinfo',
            name='dateto',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vacationinfo',
            name='description',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]