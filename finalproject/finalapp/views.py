from django.shortcuts import render, redirect
from finalapp.forms import EmployeeForm,EmployeeInfoForm,VacationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import VacationInfo,EmployeeInfo
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.dateparse import parse_date

# Create your views here.
def index(request):
    return render(request,'finalapp/index.html')

def SignUp(request):
    SignedUp = False

    if request.method == 'POST':
        employee_form = EmployeeForm(data=request.POST)
        profile_form = EmployeeInfoForm(request.POST,request.FILES)

        if employee_form.is_valid() and profile_form.is_valid():
            employee = employee_form.save()
            employee.set_password(employee.password)
            employee.save()

            profile = profile_form.save(commit=False)
            profile.user = employee

            if 'profile_pic' in request.FILES:
                print('Profile pic is found')
                profile.profile_pic = request.FILES['profile_pic']
           
            profile.save()
            SignedUp = True

        else:
            print(employee_form.errors,profile_form.errors)

    else:
        employee_form = EmployeeForm()
        profile_form = EmployeeInfoForm()

    return render(request,'finalapp/SignUp.html',{'employee_form':employee_form,'profile_form':profile_form,'SignedUp':SignedUp})

def User_Login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        employee = authenticate(username=username, password=password)

        if employee:
            if employee.is_active:
                login(request,employee)
                return render(request,'finalapp/More.html',)
            else:
                return HttpResponse('<h1>Sorry!! Your account isnt active.</h1>')
        else:
            return HttpResponse('<h1>Invalid login details. Please try again</h1>')

    else:
        return render(request,'finalapp/User_Login.html',)
    
@login_required
def Home(request):
    user=request.user
    all_members=VacationInfo.objects.filter(user_id=user.id)
    return render(request,'finalapp/Home.html',{'all':all_members})

def More(request):
    return render(request,'finalapp/More.html',)

def Profile(request):
    user=request.user
    profile=EmployeeInfo.objects.get(user_id=user.id)
    form=EmployeeInfoForm(instance=profile)
    if request.method=='POST':
        form = EmployeeInfoForm(data=request.POST,instance=profile)
        if form.is_valid():
            form.save()
           
    return render(request,'finalapp/Profile.html',{'form':form})

def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def jquery(request):
    
    return render(request,'finalapp/jquery.html',)


                    
def VacationForm(request): 
    vacation_id=request.GET.get('id')
    vacay=None
    if vacation_id:      
        vacay=VacationInfo.objects.filter(id=vacation_id).first()        
    return render(request,'finalapp/vacation.html',{'vacation':vacay})

def save_vacation(request):
    user=request.user
    id=request.POST.get('id')
    description=request.POST.get('description')
    datefrom=request.POST.get('datefrom')
    dateto=request.POST.get('dateto')
    duration=request.POST.get('duration')
    
    
    if description and datefrom and dateto and duration:
       
        if id:
            vacay=VacationInfo.objects.filter(id=id).first()
            if vacay:
                vacay.description=description
                vacay.datefrom=datefrom
                vacay.dateto=dateto
                vacay.duration=duration
                vacay.save()
                return HttpResponse("saved")
              
        else:            
            VacationInfo.objects.create(user=user,description=description,datefrom=datefrom,dateto=dateto,duration=duration)
             
            
    return HttpResponse("saved")
    
