from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class EmployeeInfo(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE,)
    Job_position = models.CharField(max_length=50,blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
    date_ofBirth=models.DateField()
    

    
class VacationInfo(models.Model):
    
    user=models.ForeignKey(User,on_delete=models.CASCADE,)
    description=models.CharField(max_length=50)
    datefrom=models.DateField()
    dateto=models.DateField()
    duration=models.CharField(max_length=50)
    
    def __str__(self):
        return self.description 