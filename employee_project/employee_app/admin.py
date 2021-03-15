from django.contrib import admin
from employee_app import models
# Register your models here.

admin.site.register(models.Employee_Profile)
admin.site.register(models.Employee_Vacation)