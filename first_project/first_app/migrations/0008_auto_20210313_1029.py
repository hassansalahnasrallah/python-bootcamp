# Generated by Django 3.1.7 on 2021-03-13 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0007_homepagemodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepagemodel',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]