from django.shortcuts import render
from django.conf.urls import url
from . import forms
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls.base import reverse
from  django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.backends import ModelBackend
from first_app.models import ProfilePageModel,HomePageModel
from datetime import datetime
from django.utils import formats
from django.db.transaction import commit
from django.contrib.auth import logout

# Create your views here.
def mainPage(request):
    context={}
    return render(request,'MainPage.html',context)
def register(request):
     user_form = forms.UserForm()
     if request.method =="POST":
         user_form = forms.UserForm(data=request.POST)
         if user_form.is_valid:
             user=user_form.save()
             user.set_password(user.password)
             user.save()

     context={"userform":user_form}
     return render(request,'signup.html',context)
     
def userLogin(request):
     context={}
     if request.method=="POST":
         username=request.POST.get('username') 
         password=request.POST.get('password')
         user = authenticate(username=username,password=password)
         if user:
             if user.is_active:
                 login(request,user)
                 return HttpResponseRedirect(reverse('vacation_table'))
             else:
                 return HttpResponse('ur account isnt active')
         else:
             return HttpResponse('Invalid Login Details')
        
     return  render(request,'login.html',context)
 

@login_required(login_url='LogIn/')
def ProfilePageView(request):  
     user=request.user
     #user_profile=User.objects.filter(id=user.id)
     user_one=ProfilePageModel.objects.all()
     employee_form=forms.ProfilePageForm
     if request.method =="POST":
         employee_form=forms.ProfilePageForm(data=request.POST)
         if employee_form.is_valid:
             employ=employee_form.save(commit=False)
             if 'profilepic' in request.FILES:
                 print("found the picture")
                 employ.profilepic=request.FILES['profilepic']
             employ.user=user
             employ.save()
             return HttpResponseRedirect(reverse('register'))
             
             
     context={"employee_form":employee_form}
     return render(request,'profilepage.html',context)
         
@login_required(login_url='LogIn/')        
def HomePageView(request):
     context={}
     user=request.user
     user_form=forms.HomePageForm
     user_id= request.GET.get("id")
     userid=None
     if user_id:
         userid=HomePageModel.objects.filter(id=user_id).first()
     context['userid']=userid
     context['user_form']=user_form
 
     return render(request,'homepage.html',context)

def savedHomePage(request):
     user=request.user
     description=request.POST.get('text_area')
     datetime_from=request.POST.get('datefrom')
     datetime_to= request.POST.get('dateto')
     Duration=request.POST.get('duration_field')
     idUserVaca=request.POST.get('idOfVaca')
     if idUserVaca:
         user_vaca=HomePageModel.objects.filter(id=idUserVaca).first()
         if user_vaca:
             user_vaca.description= description
             user_vaca.datetimefrom= datetime_from
             user_vaca.datetimeto= datetime_to
             user_vaca.Duration= Duration
             user_vaca.save()
     else:
         HomePageModel.objects.create(user=user,description=description,datetimefrom=datetime_from,datetimeto=datetime_to,Duration=Duration)
     
     return HttpResponse("Saved")

@login_required(login_url='LogIn/') 
def vacation_table(request):
     user_info=HomePageModel.objects.all()
     context={"user_info":user_info,"present_user":request.user}  
     return render(request,'vacationtable.html',context)
    
def logOutUser(request):
     logout(request)
     return HttpResponseRedirect(reverse('userLogin'))
def base_Page(request):
     context={"user":request.user}
     render(request,'base.html',context)
     
urlpatterns = [
    
     url(r'register/',register,name="register"),
     url(r'LogIn/',userLogin,name="userLogin"),
     url(r'ProfilePage/',ProfilePageView,name="ProfilePageView"),
     url(r'HomePage/',HomePageView,name="HomePageView"),
     url(r'vacation/',vacation_table,name="vacation_table"),
     url(r'savedPage/',savedHomePage,name="savedHomePage"),
     url(r'mainPage/',mainPage,name="mainPage"),
     url(r'logOut/',logOutUser,name="logOutUser"),
    url(r'base_Page/',base_Page,name="base_Page"),
    ]