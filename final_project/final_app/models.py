from django.db import models
from django.template.defaultfilters import default
from django.contrib.auth.models import User
from django.db.models.base import Model

class UserProfileInfo(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job_position = models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    Date_Of_Birth = models.DateField()
    
    
    

class Vacation(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    date_from = models.DateField()
    date_to = models.DateField()