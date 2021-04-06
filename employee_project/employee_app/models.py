from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Employee_Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    job_position = models.CharField(max_length=255)
    employe_profile = models.ImageField(upload_to='profile_pics',blank=True)
    birth_date = models.DateField(blank=True, null=True)
    
class Employee_Vacation(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    Description = models.CharField(max_length=255)
    Datetime_From = models.DateField()
    Datetime_To = models.DateField()
    status=models.BooleanField(default=True)
    Duration = models.IntegerField(default=0)