from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserProfile(models.Model): 
     user = models.OneToOneField(User,on_delete=models.CASCADE)
     
     position = models.CharField(max_length=20)
     picture = models.ImageField(upload_to='profile_pics',blank=True)
     
     
     
class Vacation(models.Model):
    description=models.CharField(max_length=255)
    date_from = models.DateField()
    date_to= models.DateField()
    duration=models.CharField(max_length=10)
       