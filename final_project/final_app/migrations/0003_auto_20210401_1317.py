# Generated by Django 3.1.7 on 2021-04-01 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final_app', '0002_auto_20210320_1121'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofileinfo',
            old_name='Date_Of_Birth',
            new_name='date_of_birth',
        ),
        migrations.RenameField(
            model_name='vacation',
            old_name='user',
            new_name='employee',
        ),
        migrations.AddField(
            model_name='vacation',
            name='duration',
            field=models.CharField(default=None, max_length=10),
        ),
        migrations.AddField(
            model_name='vacation',
            name='status',
            field=models.BooleanField(default=None),
        ),
        migrations.AlterField(
            model_name='vacation',
            name='description',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
