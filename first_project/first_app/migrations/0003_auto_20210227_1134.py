# Generated by Django 3.1.7 on 2021-02-27 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0002_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(blank=True, upload_to='profile_pics'),
        ),
    ]
