# Generated by Django 3.1.7 on 2021-03-13 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finalapp', '0004_remove_vacationinfo_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacationinfo',
            name='duration',
            field=models.CharField(default=2, max_length=50),
            preserve_default=False,
        ),
    ]
