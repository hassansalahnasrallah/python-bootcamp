from django import forms
from employee_app.models import Employee_Profile
from django.contrib.auth.models import User
BIRTH_YEAR_CHOICES=list(range(1900,2021))
class UserForm(forms.ModelForm):     
    password=forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model=User
        fields=('username','email','password','first_name','last_name')
      
class UserProfileForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))    
    class Meta():
        model=Employee_Profile
        fields=('job_position','employe_profile','birth_date')

