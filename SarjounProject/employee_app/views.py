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

@login_required()
def home(request):
    username=request.POST.get('username')
    context={'username':username}
    return render(request,'home.html',context)


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
    return HttpResponseRedirect(reverse('home'))

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
    status='OK'
    message='SUCCESS'
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
        else:
            message="MISSING_RQUIRED_PARAMETERS"
            status="FAIL"
        
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
    url(r'home/',home,name='home'),
    url(r'vacation/',vacation,name='vacation'),
    url(r'AddV',AddV,name='AddV'),
    url(r"save/",save,name="save")
    ]