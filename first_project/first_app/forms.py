from  django.contrib.auth.models import User
from django import forms
from first_app.models import ProfilePageModel,HomePageModel
from django.forms.widgets import DateInput,Textarea
class UserForm(forms.ModelForm):
      password = forms.CharField(widget=forms.PasswordInput())
      class Meta():
         model= User
         fields= ("username","first_name","last_name","email","password")

class DateInput(forms.DateInput):
     input_type = 'date'
    
class ProfilePageForm(forms.ModelForm):
     class Meta():
         model=ProfilePageModel
         fields=("jobposition","profilepic","dateOfBirth")
         widgets={
             "dateOfBirth": DateInput()
             
             }
         
class HomePageForm(forms.ModelForm):
     class Meta():
         model=HomePageModel
         fields=("description","datetimefrom","datetimeto","Duration")
         widgets={
             "datetimefrom":DateInput(),
             "datetimeto":DateInput(),
             "description":Textarea(attrs={'cols': 80, 'rows': 10})
             
             }