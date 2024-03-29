from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    
    topic_name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.topic_name
    

class Webpage(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    url = models.URLField(unique=True)
    
    def __str__(self):
        return self.name
    

class AccessRecord(models.Model):
    webpage_name = models.ForeignKey(Webpage, on_delete=models.CASCADE)
    date = models.DateField()
    
    def __str__(self):
        return str(self.date)
    
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    portfolio = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_pics', blank=True)    
    
