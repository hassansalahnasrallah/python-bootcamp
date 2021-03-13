from django.shortcuts import render, redirect
from finalapp.forms import EmployeeForm,EmployeeInfoForm,VacationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import VacationInfo,EmployeeInfo
from django.contrib.auth.models import User


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

def EditVacay(request,pk=None):
    if pk:
        vacay=VacationInfo.objects.get(id=pk) 
        form=VacationForm(instance=vacay)
    if request.method=='POST':
        form = VacationForm(data=request.POST,instance=vacay)
        if form.is_valid():
            form.save()
    return render(request,'finalapp/EditVacay.html',{'form':form})

def Vacation(request):
    added=False
    datefrom=None
    dateto=None
    if request.method == 'POST':
        vacation_form = VacationForm(data=request.POST)
       # datefrom=None
       # dateto=None
        if vacation_form.is_valid():
          # datefrom=vacation_form.cleaned_data(['datefrom'])
           #dateto=vacation_form.cleaned_data(['dateto'])
           vacation = vacation_form.save(commit=False)
           emp=request.user
           vacation.user=emp
           vacation.save()
          
           added=True
           datefrom=vacation_form.cleaned_data['datefrom']
           dateto=vacation_form.cleaned_data['dateto']
           
        else:
            print(vacation_form.errors)
       
    else:
        vacation_form = VacationForm()
       
    return render(request,'finalapp/vacation.html',{'form':vacation_form,'added':added,'datefrom':datefrom,'dateto':dateto})