from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default='static/images/df.png')
    position = models.CharField(max_length=255)
    date_of_birth = models.DateField()

    def __str__(self):
        return str(self.user)


class Vacation(models.Model):
    #emp_name = models.ForeignKey(User,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    desc = models.CharField(max_length=255)
    from_date = models.DateField()
    to_date = models.DateField()

    def __str__(self):
        return self.desc
