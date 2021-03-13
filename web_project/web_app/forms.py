from django import forms
from web_app.models import User, Userprofile, Vacation
# from django.contrib.auth.models import User
from tkinter.test.support import widget_eq
from web_app import models
from dataclasses import fields



class UserForm(forms.ModelForm):
#
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('first_name', 'last_name' , 'email' , 'username' , 'password')
        
        
        
        
class UserProfileInfoForm(forms.ModelForm):
    
    class Meta():
        model = Userprofile
        fields = ('job_description' , 'picture', 'date' )
        widgets = {
            'date': forms.DateInput(attrs={'class':'datepicker'}),
        }
        
        
        
        
class vacation(forms.ModelForm):
    class Meta():
        model = Vacation
        fields = ('description', 'datefrom', 'dateto')