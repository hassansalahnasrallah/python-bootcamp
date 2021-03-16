from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from MySQLdb.constants.ER import REQUIRES_PRIMARY_KEY

# Create your models here.
class UserProfile(models.Model):
    
    user=models.OneToOneField(User, on_delete=CASCADE)
    picture =models.ImageField(upload_to='profile_pics', blank=True)

class Vacation(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    description=models.CharField(max_length=255,unique=True)
    datefrom=models.DateField()
    dateto=models.DateField()