# Generated by Django 3.1.7 on 2021-03-24 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('final_app', '0011_auto_20210322_1735'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vacation',
            old_name='from_date',
            new_name='datefrom',
        ),
        migrations.RenameField(
            model_name='vacation',
            old_name='to_date',
            new_name='dateto',
        ),
        migrations.RenameField(
            model_name='vacation',
            old_name='job_desc',
            new_name='vacation_desc',
        ),
    ]
