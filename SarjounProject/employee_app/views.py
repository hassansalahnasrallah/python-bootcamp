from django.shortcuts import render
from django.conf.urls import url
from django.http.response import HttpResponse, HttpResponseRedirect
from . import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse
from employee_app.models import Vacation,UserProfile
from django.contrib.auth.models import User
import json
from django.db.utils import IntegrityError
# Create your views here.

def Login(request):
    context={}
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        
        if user:
            if user.is_active:
                login(request,user)
                print("user active")
                return HttpResponseRedirect(reverse('vacation'))
            else:
                return HttpResponse("Not connected")
        else:
            return HttpResponse("User not found")
    else:
         return render(request,'login.html', context)
    
    return render(request,'login.html',context)


def Signup(request):
    userprofileinfo=forms.userprofile()
    signup_form=forms.FormSignup()
    sign_up=False
    
    if request.method=='POST':
        signup_form=forms.FormSignup(data=request.POST)
        userprofileinfo=forms.userprofile(data=request.POST)
        
        if signup_form.is_valid() and userprofileinfo.is_valid():
            user=signup_form.save()
            user.set_password(user.password)
            user.save()
            profile=userprofileinfo.save(commit=False)
            profile.user=user
            profile.save()
            sign_up=True
            return HttpResponseRedirect(reverse('login'))
        else:
             print("User not found")
    else:
        print("Not valid")

    context={'signup_form':signup_form,'sign_up':sign_up,'userinfo':userprofileinfo}

    return render(request,'signup.html',context)

@login_required
def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

@login_required()
def EditProfile(request):
    context={}
    user_id=request.GET.get('id')
    user_profile=None
    if user_id:
        user_profile=UserProfile.objects.filter(id=user_id).first()
    context['vacation']=vacation
    return render(request,'EditProfile.html',context)

def save_profile(request):
    user=request.user
    job_position=request.POST.get("Jposition")
    dateofbirth=request.POST.get("date_of_birth")
    profilepicture=request.POST.get("P-pic")
    user_id=request.POST.get("user_id")
    if job_position and dateofbirth and profilepicture:
        if vacation_id:
            user_profile=UserProfile.objects.filter(id=user_id).first()
            if vacation:
                user_profile.job_position=job_position
                user_profile.dateofbirth=dateofbirth
                user_profilepicture=profilepicture
                user_profile.save()
        else:
            UserProfile.objects.create(user=user,job_position=job_position,dateofbirth=dateofbirth,profilepicture=profilepicture)
    return HttpResponseRedirect(reverse('vacation'))


@login_required()
def vacation(request):
    context={}
    context['vacations']=Vacation.objects.all()
    return render(request,'vacation.html',context)


@login_required()
def AddV(request):
    context={}
    vacation_id=request.GET.get('id')
    vacation=None
    if vacation_id:
        vacation=Vacation.objects.filter(id=vacation_id).first()
    context['vacation']=vacation
    return render(request,'Addv.html',context)


def save(request):
    user=request.user
    description=request.POST.get("desc")
    datefrom=request.POST.get("date_from")
    dateto=request.POST.get("date_to")
    vacation_id=request.POST.get("vacation_id")
    status="OK"
    message="SUCCESS"
    payload={}
    try:
        if description and datefrom and dateto:
            if vacation_id:
                vacation=Vacation.objects.filter(id=vacation_id).first()
                if vacation:
                    vacation.description=description
                    vacation.datefrom=datefrom
                    vacation.dateto=dateto
                    vacation.save()
                    payload['id']=vacation.id
                else:
                    message="VACATION_NOT_FOUND"
                    status="FAIL"
            else:
                Vacation.objects.create(user=user,description=description,datefrom=datefrom,dateto=dateto)
    except IntegrityError:
        message="VACATION_NAME_DUPLICATE"
        status="FAIL"
    except:
        message="SYSTEM_ERROR"
        status="FAIL"
    response={"status":status,"message":message,"payload":payload}
    return HttpResponseRedirect(reverse('vacation'))

urlpatterns=[
    url(r'login/',Login,name='login'),
    url(r'logout/',Logout,name='logout'),
    url(r'signup/',Signup,name='sign_up'),
    url(r'EditProfile/',EditProfile,name='EditProfile'),
    url(r'vacation/',vacation,name='vacation'),
    url(r'AddV',AddV,name='AddV'),
    url(r"save/",save,name="save"),
    url(r"save_profile/",save_profile,name="save_profile"),
    ]