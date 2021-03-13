from django import forms
from django.contrib.auth.models import User
from final_app.models import ProfileContent, Vacation

#class LoginPage_form(forms.ModelForm):
    
#    password=forms.CharField(widget=forms.PasswordInput())
#    class Meta():
#        model=User
#        fields=( 'username' , 'password' )
    
class UserProfile_form(forms.ModelForm):
    
    password=forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model=User
        fields=('username' ,  'first_name' , 'last_name' , 'email' , 'password' )
        
class Vacation_form(forms.ModelForm):
    class Meta():
        model=Vacation
        fields=('job_desc' , 'from_date' , 'to_date')        
#class UserProfile_form(forms.ModelForm):
    
#    password=forms.CharField(widget=forms.PasswordInput())
#    class Meta():
#        model=UserData
#        fields=('username' ,  'first_name' , 'last_name' , 'email' , 'password' )
        
class ProfileContent_form(forms.ModelForm):
    class Meta():
        model=ProfileContent
        #fields=('job_position' ,  'profile_pic')
        fields=('job_position' ,  'profile_pic' , 'date_of_birth' )
    