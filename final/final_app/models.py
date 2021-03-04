from django.db import models


class Employees(models.Model):
    employee_name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.employee_name

class Vacations(models.Model):
    discripton= models.CharField(max_length=255, unique=True)
    date_from= models.DateField()
    date_to= models.DateField()
    
    def __str__(self):
        return self.date_from
    
    
    
    