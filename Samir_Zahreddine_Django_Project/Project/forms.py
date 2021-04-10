from django import forms

from Vacations.models import *
from Project import settings
from datetime import *
from django.forms.widgets import*
from django.db.models.fields import CharField



class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())
    class Meta():
        model = User
        fields =('username','email','password')
        #fields = ('username','email','profile_pic')

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = EmployeeProfile
        fields = ('profile_pic','position','date_of_birth')
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'}), 
        }  


class UserForm1(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())
    class Meta():
        model = User
        fields =('email','password')
     



class VacationInfoForm(forms.ModelForm):
    class Meta(): #same Consept as __init__
        model = Vacation
        fields = ('desc','from_date','to_date')   
        #fields = ('__all__')
        widgets = {
            'from_date': DateInput(attrs={'type': 'date'}),
            'to_date': DateTimeInput(attrs={'type': 'date'}),
        }    