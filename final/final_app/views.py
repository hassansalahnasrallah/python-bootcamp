from django.conf.urls import url
from django import forms
from django.http.response import HttpResponse
from . import forms
from django.shortcuts import render

def register(request):
    user_form = forms.UserForm
    profile_form = forms.UserProfileInfoForm
    if request.method == "POST":
        user_form = forms.UserForm(data=request.POST)
        profile_form = forms.UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            # save the user
            user = user_form.save()
            # hash the password
            user.set_password(user.password)
            
            user.save()
        
            
            profile = profile_form.save(commit=False)
            if 'picture' in request.FILES:
                print("Found the picture")
                profile.picture = request.FILES['picture']
            
            profile.user = user
            profile.save()
        else:print('form nor valid')
        
            
    context = {'forms': forms.UserForm, 'profile_form': forms.UserProfileInfoForm}
    return render(request, 'signup.html', context)
 

urlpatterns = [
    url(r"register", register, name="register"),
    ]