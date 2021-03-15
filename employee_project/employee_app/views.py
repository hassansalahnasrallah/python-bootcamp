from django.shortcuts import render
from django.http.response import HttpResponse,HttpResponseRedirect
from django.conf.urls import url
from employee_app import forms
from django.template.context_processors import request
from django.contrib.auth import authenticate,login, logout
from django.urls.base import reverse
from django.contrib.auth.decorators import login_required
from employee_app.models import Employee_Vacation 
from django.contrib import messages
from django.http import response
# Create your views here.

def Main(request):
    context={}
    return render(request,"employee_app/Home.html", context)

def Sign_Up_Form(request):
    userinfo=forms.UserForm()
    profileinfo=forms.UserProfileForm()
    if request.method == 'POST':
         userinfo=forms.UserForm(data=request.POST)
         profileinfo=forms.UserProfileForm(data=request.POST)
         if userinfo.is_valid() and profileinfo.is_valid():
             user = userinfo.save()
             user.set_password(user.password)
             user.save()
             profile = profileinfo.save(commit=False)
             profile.user = user
             if 'employe_profile' in request.FILES:
                print('found it')
                profile.employe_profile = request.FILES['employe_profile']
             profile.save()
         else:
             print("Not Valid")
    else:
        print("Not valid request")            
    context={"user_form":userinfo,"profile_form":profileinfo}
    return render(request,"employee_app/sign_up.html", context)

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)

                return HttpResponseRedirect(reverse('Vacation_Table'))
            else:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'employee_app/login.html', {})


@login_required
def Vacation_Fields(request):
        context={}    
        vacation_id=request.GET.get('id')
        vacation=None
        if vacation_id:
            vacation=Employee_Vacation.objects.filter(id=vacation_id).first()
        context['vacation']=vacation   
        return render(request,"employee_app/Vacation_requirments.html",context)
    
def Vacation_save(request):
     user=request.user
     Description=request.POST.get("desc")
     Date_From=request.POST.get("datefrom")
     Date_To=request.POST.get("dateto")
     Duration=request.POST.get("duration_d")
     vacation_id=request.POST.get("vacation_id")
     if Description and Date_From and Date_To :
          if vacation_id:
             vacation=Employee_Vacation.objects.filter(id=vacation_id).first()
             if vacation:
                 vacation.Description=Description
                 vacation.Datetime_From=Date_From
                 vacation.Datetime_To=Date_To
                 vacation.save()
                 response="Success"
             else: response="Fail"
          else:
              Employee_Vacation.objects.create(user=user,Description=Description,Datetime_From=Date_From,Datetime_To=Date_To)
              response="Success"
     else:
         response="Fail"
     return HttpResponse(response)

@login_required
def Vacation_Table(request):
     context={}
     context["vacations"]=Employee_Vacation.objects.all()
     return render(request,"employee_app/Vacation_table.html",context)
 
@login_required
def employee_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Main'))
    
    
urlpatterns=[
    url(r'Main/',Main,name='Main'),
    url(r'Sign_up/',Sign_Up_Form,name='Sign_Up_Form'),
    url(r'login/',user_login,name='user_login') ,
    url(r'Vacation_Fields/', Vacation_Fields,name='Vacation_Fields') ,
    url(r'Vacation_Table/', Vacation_Table,name='Vacation_Table') ,
    url(r'Vacation_save/', Vacation_save,name='Vacation_save') ,
    url(r'logout/',employee_logout,name='employee_logout') 
    
    ]