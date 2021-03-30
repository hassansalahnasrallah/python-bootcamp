from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class UserProfile(models.Model): 
     user = models.OneToOneField(User, on_delete=models.CASCADE)
     
     position = models.CharField(max_length=20)
     picture = models.ImageField(upload_to='profile_pics', blank=True)
     date_of_birth = models.DateField(null= True)
     
     
     
class Vacation(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, null = True)
    duration = models.CharField(max_length=10,default = None)
    date_from = models.DateField()
    date_to = models.DateField()
    status = models.BooleanField(default = None)
    
       