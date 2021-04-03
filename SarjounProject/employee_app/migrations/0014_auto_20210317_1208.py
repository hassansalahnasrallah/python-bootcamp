# Generated by Django 3.1.7 on 2021-03-17 10:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employee_app', '0013_auto_20210315_1347'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='dateofbirth',
            field=models.DateField(),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='job_position',
            field=models.CharField(default='NA', max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
