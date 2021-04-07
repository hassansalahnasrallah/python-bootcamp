from django import forms
from final_app.models import User, UserProfile, Vacation
from django.contrib.auth.models import User
from tkinter.test.support import widget_eq
from final_app import models
from dataclasses import fields



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    
    class Meta():
        model = User
        fields = ('first_name', 'last_name' , 'email' , 'username' , 'password')
        
        
        
        
class UserProfileInfoForm(forms.ModelForm):
    
    class Meta():
        model= UserProfile
        fields=('job_position', 'profile_pic', 'date_of_birth')
        
        
        
        
        
class VacationForm(forms.ModelForm): 
    class Meta():
        model = Vacation   
        fields ='__all__'