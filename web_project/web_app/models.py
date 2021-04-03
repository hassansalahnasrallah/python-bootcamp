from django.db import models
from django.template.defaultfilters import default
from django.contrib.auth.models import User


class Userprofile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    job_description=models.CharField(max_length=255)
    picture=models.ImageField(upload_to='profile_pics', blank=True)
    
    
    
    

class Vacation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description=models.CharField(max_length=255)
    datefrom=models.DateField()
    dateto=models.DateField()