from django.shortcuts import render
#from django.http.response import HttpResponse
# Create your views here.
from django.conf.urls import url 
from final_app.models import ProfileContent, Vacation
from . import forms
from django.template.context_processors import request
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls.base import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import json
from django.db.utils import IntegrityError

def MainPage(request):
    
    context={}
    return render(request, 'final_app/mainpage.html', context)


#def VacationPage(request):
#    user=request.user
#    user_vacation=forms.Vacation_form
#    if request.method=="POST":
#        user_vacation=forms.Vacation_form(data=request.POST)
#        if user_vacation.is_valid:
#            uservacation=user_vacation.save(commit=False)
#            uservacation.user_id=request.user.id 
#            uservacation.save()
#            return HttpResponseRedirect(reverse('profilepage'))
#    context={"user_vacation":user_vacation}
#    return render(request, 'final_app/vacation.html', context)
    
def LoginPage(request):
    
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
"""
def Vacation(request):
    vac_added=False
    datefrom=None
    dateto=None
    vacation_form = forms.Vacation()
    if request.method == 'POST':
        vacation_form = forms.Vacation(data=request.POST)

        if vacation_form.is_valid():
         
           vacation = vacation_form.save(commit=False)
           vacation.user = request.user
           
           vacation.save()
          
           vac_added=True
           
           date_from=vacation_form.cleaned_data['datefrom']
           date_to=vacation_form.cleaned_data['dateto']
           
        else:
            print(vacation_form.errors)
       
    #else:
       # vacation_form = Vacation_form()
    context= {'vacation_form':vacation_form,'vac_added':vac_added,'from_date':date_from,'to_date':date_to}
    
    return render(request,'final_app/vacation.html', context)
"""
@login_required
def logout(request):
    
    return HttpResponseRedirect(reverse('loginPage'))


@login_required
def vacation_form_view(request):
    context={}
    context['vacations']=Vacation.objects.all()
    
    return render(request,'final_app/vacationtable.html',context)

@login_required()
def add_vacation(request):
    context={}
    vacation_id=request.GET.get('id')
    vacation=None
    if vacation_id:
        vacation=Vacation.objects.filter(id=vacation_id).first()
    context['vacation']=vacation
    return render(request,'final_app/vacation.html',context)


def save(request):
    """
    """
    
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
                vacation = Vacation.objects.filter(id=vacation_id).first()
            else:
                vacation = Vacation(user=user)
                
            if vacation:
                vacation.description = description
                vacation.datefrom = datefrom
                vacation.dateto = dateto
                vacation.save()
                
                payload['id'] = vacation.id
                
            else:
                message="VACATION_NOT_FOUND"
                status="FAIL"
        else:
            #Use logging
            message="MISSING_REQUIRED_PARAMETERS"
            status="FAIL"
            
    except IntegrityError:
        message="VACATION_NAME_DUPLICATE"
        status="FAIL"
    except:
        message="SYSTEM_ERROR"
        status="FAIL"
        
    response={"status":status, "message":message, "payload":payload}
    
    return HttpResponse(json.dumps(response))


urlpatterns=[
    url(r"LoginPage/", LoginPage, name="loginPage"),
    url(r"mainpage/", MainPage, name="mainpage"),
    url(r"profilepage/", ProfilePage, name="profilepage"),
    url(r"register/", register, name="register"),
    url(r"user_vacation/", Vacation, name="Vacation"),
    url(r"logout/", logout, name="logout"),
    url(r"vacation_form_view/", vacation_form_view, name="vacation_form_view"),
    url(r"add_vacation/", add_vacation, name="add_vacation"),
    url(r"save/", save, name="save"),

    ]