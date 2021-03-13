from django.db import models
#import datetime
from django.contrib.auth.models import User
#from MySQLdb import DATETIME
#from django.template.defaultfilters import default
from django import forms

# Create your models here.
#class UserData(models.Model):
#    username=models.CharField(max_length=255, unique=True)
#    email=models.EmailField(unique=True)
#    first_name=models.CharField(max_length=255)
#    last_name=models.CharField(max_length=255)
#    password=models.CharField(max_length=255)
    
    
    
class ProfileContent(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    
    job_position=models.CharField(max_length=255)
    profile_pic=models.ImageField(upload_to='profile_pics', blank=True)
    
    date_of_birth=models.CharField(max_length=10, blank=True)
    
    
class Vacation(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    job_desc= models.CharField(max_length=255, blank=True)
    from_date=models.DateField()
    to_date=models.DateField()
    
     