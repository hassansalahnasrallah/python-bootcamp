from django.conf.urls import url
from django.shortcuts import render
from django import forms
from django.http.response import HttpResponse
def register(request):
    
#  context = {"user_forms": forms.UserForm, 'profile_form' : forms.UserProfileInfoForms}
   context={}
   return render(request, 'signup.html', context)

urlpatterns = [
    
    url(r"register/", register, name="register")
    
]