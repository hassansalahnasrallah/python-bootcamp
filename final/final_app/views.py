from django.conf.urls import url
from django import forms
from django.http.response import HttpResponse, HttpResponseRedirect
from . import forms
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.urls.base import reverse

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
 
def user_login(request):
    
    context = {}
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse('your account is not active')
        
        else:
            return HttpResponse("invalid login details")
    else:
        return render(request, "login.html", context)
    return render(request, "login.html", context )


def vacation_form(request):
    
    context = {}
    
    return render(request, "home.html", context )
    
def save_vacation(request):
    
    context = {}
    
    return render(request, "home.html", context )

def Example(request):
    
    context = {}
    
    return render(request, "profile.html", context )



urlpatterns = [
    url(r"register", register, name="register"),
    url(r"user_login", user_login, name="user_login"),
    url(r"home", register, name="home"),
    url(r"vacation_form", vacation_form, name="vacation_form"),
    url(r"save_vacation", save_vacation, name="save_vacation"),
    url(r"Example", Example, name="Example")

    ]

