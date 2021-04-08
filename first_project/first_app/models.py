from django.db import models
from  django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
import datetime

# Create your models here.
class ProfilePageModel(models.Model):
     user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
     jobposition=models.CharField(max_length=255)
     profilepic=models.ImageField(upload_to='profile_pics',blank=True)
     dateOfBirth=models.DateField()
     
class HomePageModel(models.Model):
     id=models.AutoField(primary_key=True)
     user=models.ForeignKey(User,on_delete=models.CASCADE)
     description=models.TextField()
     datetimefrom=models.DateField()
     datetimeto=models.DateField()
     status=models.BooleanField(default=True)
     Duration=models.IntegerField(default=0)
     
      