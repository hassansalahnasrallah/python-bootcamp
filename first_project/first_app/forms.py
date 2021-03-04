from django import forms
from first_app.models import Webpage, UserProfile
from django.contrib.auth.models import User

class FormName(forms.Form):
    name=forms.CharField()
    email=forms.EmailField()
    verify_email=forms.EmailField(label='Enter your email again')
    text=forms.CharField(widget=forms.Textarea)
    
    def clean(self):
        all_clean_data=super().clean()
        
        #email=all_clean_data['email']
       # vmail=all_clean_data['verify_email']
        
        if email!= vmail:
            raise forms.ValidationError("Make sure emails match")

class WebpageForm(forms.ModelForm):
    class Meta():
        model=Webpage
        fields='__all__' 

class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    
    class Meta():
        model=User
        fields=('username','email','password','first_name','last_name')
        
    class UserProfileInfoForm(forms.ModelForm):
        class Meta():
            model=UserProfile
            fields=('portfolio','picture')
            