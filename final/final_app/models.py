from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE


class UserProfile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_pics', blank=True)
    def __str__(self): 
        return self.User

class Vacations(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    discripton= models.CharField(max_length=255, unique=True)
    date_from= models.DateField()
    date_to= models.DateField()
    
    def __str__(self):
        return self.Vacations
    
    
    
    