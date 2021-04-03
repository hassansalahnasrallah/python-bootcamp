from django.db import models
from django.contrib.auth.models import User

# Create your models here.

    
class EmployeeProfile(models.Model):
    Employee=models.OneToOneField(User,on_delete=models.CASCADE)
    JobPosition=models.CharField(max_length=255)
    DateOfBirth=models.DateField()
    picture=models.ImageField(upload_to='profile_pics',blank=True)
    
class Vacation(models.Model):
    Employee=models.ForeignKey(User,on_delete=models.CASCADE)
    Description=models.CharField(max_length=255)
    DateFrom=models.DateField()
    DateTo=models.DateField()
    Status= models.BooleanField(default=True)
    
    @property
    def duration(self):
        return(Dateto-DateFrom).days
  