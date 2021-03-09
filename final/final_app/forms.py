from django import forms
from django.contrib.auth.models import User
from final_app.models import UserProfile 


class formName(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    verify_email = forms.EmailField()

class UserForm(forms.ModelForm):
    password= forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username', 'email', 'password', 'first_name','last_name')
    
class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfile
        fields = ('picture',)