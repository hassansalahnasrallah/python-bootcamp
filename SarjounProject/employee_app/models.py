from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
# Create your models here.
class UserProfile(models.Model):
    
    user=models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    
    job_position=models.CharField(max_length=255)
    profile_pic =models.ImageField(upload_to='profile_pics', blank=True)
    

class Vacation(models.Model):
    id=models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    description = models.CharField(max_length=255, null=True)
    duration = models.IntegerField(default=0, null=True)
    datefrom = models.DateField(null=True)
    dateto = models.DateField(null=True)
    status = models.BooleanField(default=True)