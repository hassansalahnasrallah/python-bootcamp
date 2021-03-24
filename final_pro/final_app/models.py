from django.db import models
#import datetime
from django.contrib.auth.models import User
#from MySQLdb import DATETIME
#from django.template.defaultfilters import default
from django import forms
from MySQLdb.constants.ER import REQUIRES_PRIMARY_KEY

# Create your models here.

    
class ProfileContent(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    
    job_position=models.CharField(max_length=255)
    profile_pic=models.ImageField(upload_to='profile_pics', blank=True)
    
    date_of_birth=models.DateField(blank= True)
    
    
class Vacation(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    vacation_desc= models.CharField(max_length=255)
    datefrom=models.DateField()
    dateto=models.DateField()
    Duration=models.IntegerField(default=0)
    
     