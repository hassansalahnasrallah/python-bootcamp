from django import forms
from django.contrib.auth.models import User
from employee_app.models import UserProfile

class FormSignup(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    
    class Meta():
        model=User
        fields=('username','email','password')
        
class userprofile(forms.ModelForm):
    class Meta():
        model=UserProfile
        fields='__all__'
    