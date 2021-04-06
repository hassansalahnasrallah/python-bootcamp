from django import forms
from pro_app.models import UserProfile, Vacation
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    
    password=forms.CharField(widget=forms.PasswordInput())
    
    class Meta():
        model = User
        fields =('username','email','password','first_name','last_name')
           
class UserProfileInfoForm(forms.ModelForm):
    
    class Meta():
        model= UserProfile
        fields=('position', 'picture', 'date_of_birth')   
        

class VacationForm(forms.ModelForm): 
    class Meta():
        model = Vacation   
        fields ='__all__'  