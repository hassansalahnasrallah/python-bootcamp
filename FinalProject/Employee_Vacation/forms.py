from django import forms
from django.contrib.auth.models import User
from Employee_Vacation.models import EmployeeProfile

from Employee_Vacation.models import Vacation

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password')
        
class EmployeeProfileForm(forms.ModelForm):
    class Meta():
        model = EmployeeProfile
        fields = ('JobPosition','DateOfBirth','picture')
        
class EmployeeVacationForm(forms.ModelForm):
    class Meta():
        model = Vacation
        fields = ('Description','DateFrom','DateTo')