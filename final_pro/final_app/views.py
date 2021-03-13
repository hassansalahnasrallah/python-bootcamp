from django.shortcuts import render
#from django.http.response import HttpResponse
# Create your views here.
from django.conf.urls import url 
from . import forms
from django.template.context_processors import request
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.urls.base import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def MainPage(request):
    
    context={}
    return render(request, 'final_app/mainpage.html', context)


def VacationPage(request):
    user=request.user
    user_vacation=forms.Vacation_form
    if request.method=="POST":
        user_vacation=forms.Vacation_form(data=request.POST)
        if user_vacation.is_valid:
            uservacation=user_vacation.save(commit=False)
            uservacation.user=user 
            uservacation.save()
            return HttpResponseRedirect(reverse('profilepage'))
    context={"user_vacation":user_vacation}
    return render(request, 'final_app/vacation.html', context)
    
def LoginPage(request):
    #user_login=forms.LoginPage_form
    #context={"user_login": user_login}
    context={}
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                
                return HttpResponseRedirect(reverse('profilepage'))
            else:
                return HttpResponse("your account is not active")
        else:
            return HttpResponse("invalid login details")
                
    else:
        return render(request, 'final_app/login.html', context)
    
   # return render(request, 'final_app/login.html', context)

#def index(request):
#    context={"i":"."}
#    return render(request, "final_app/mainpage.html", context)
@login_required
def ProfilePage(request):
    #form_user=forms.UserProfile_form()
    user=request.user
    UserProfile=User.objects.filter(id=user.id)
    user_form=forms.ProfileContent_form
    
    if request.method=="POST":
        user_form=forms.ProfileContent_form(data=request.POST)
        if user_form.is_valid:
            employee=user_form.save(commit=False)
            if 'profile_pic' in request.FILES:
                print("found the pic")
                employee.profile_pic= request.FILES['profile_pic']
            employee.user=user
            employee.save()
              
        
    context={"user_form":user_form}
    return render(request, 'final_app/profile_page.html', context)


def register(request):
    user_form=forms.UserProfile_form
    profile_form=forms.ProfileContent_form
    
    registered= False
    if request.method=="POST":
        user_form=forms.UserProfile_form(data=request.POST)
        profile_form=forms.ProfileContent_form(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()
            
            profile = profile_form.save(commit=False)
            
            if 'profile_pic' in request.FILES:
                print("found the pic")
                profile.profile_pic= request.FILES['profile_pic']
            
            profile.user=user
            profile.save()
            
            registered=True
        else:
            print("form not valid")
            
    else:
        print("not valid request")
    context={"user_form":forms.UserProfile_form , "profile_form" : forms.ProfileContent_form , "registered": registered}
    return render(request, 'final_app/new_account.html', context)

urlpatterns=[
    url(r"loginpage/",LoginPage,name="loginPage"),
   # url(r"newaccount/",NewAccountPage, name="newaccount"),
    url(r"mainpage/",MainPage, name="mainpage"),
    url(r"profilepage/",ProfilePage, name="profilepage"),
    url(r"register/",register, name="register"),
    url(r"user_vacation/",VacationPage,name="VacationPage"),
    ]