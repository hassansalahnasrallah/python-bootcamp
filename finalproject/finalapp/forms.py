from django import forms
from django.contrib.auth.models import User
from finalapp.models import EmployeeInfo,VacationInfo

class EmployeeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password')


class EmployeeInfoForm(forms.ModelForm):
    class Meta():
        model = EmployeeInfo
        fields = ('Job_position','profile_pic','date_ofBirth')
    

        
class VacationForm(forms.ModelForm):
    class Meta():
        model = VacationInfo
        fields = ('description','datefrom','dateto','duration')
