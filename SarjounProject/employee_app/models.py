from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from MySQLdb.constants.ER import REQUIRES_PRIMARY_KEY

# Create your models here.
class UserProfile(models.Model):
#<<<<<<< HEAD
    user=models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    job_position=models.CharField(max_length=255)
    dateofbirth=models.DateField()
    profilepicture =models.ImageField(upload_to='profile_pics', blank=True)
#=======
    id=models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    job_position = models.CharField(max_length=255)
    dateofbirth = models.DateField()
    profilepicture = models.ImageField(upload_to='profile_pics', blank=True)
#>>>>>>> 0560c512d57fcde4e93c00f505fe3ea9595876c4

class Vacation(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=255,unique=True)
    datefrom = models.DateField()
    dateto = models.DateField()
    #