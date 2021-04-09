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
from django.core.serializers.json import DjangoJSONEncoder
from first_project import settings
import json
import logging
from telnetlib import theNULL
from builtins import int
from django.db.models import Q
import random
from _datetime import date
import os
# Create your views here.

log = logging.getLogger(__name__)

def mainPage(request):
    context={}
    return render(request,'MainPage.html',context)
def register(request):
     try:
         user_form = forms.UserForm()
         if request.method =="POST":
             user_form = forms.UserForm(data=request.POST)
             if user_form.is_valid:
                 user=user_form.save()
                 user.set_password(user.password)
                 user.save()
                 return HttpResponseRedirect(reverse('userLogin'))
                 log.debug("You have  registered successfully " )
     except:
         log.debug("Error while registering")     
     context={"userform":user_form}
     return render(request,'signup.html',context)
     
def userLogin(request):
     try:
         context={}
       
         if request.method=="POST":
             username=request.POST.get('username') 
             password=request.POST.get('password')
             user = authenticate(username=username,password=password)
             if user:
                 if user.is_active:
                     login(request,user)
                     log.debug("Welcome You have LogIn ")
                     return HttpResponseRedirect(reverse('vacation_table'))
                 else:
                     return HttpResponse("Your account is not active.")
                     
             else:
                 log.debug("Someone tried to login and failed.")
                 log.debug("They used username: {} and password: {}".format(username,password))
                 return HttpResponse("Invalid login details supplied.")
     except:
         log.debug("Error while logIn")            
    
     return  render(request,'login.html',context)
 

@login_required(login_url='LogIn/')
def ProfilePageView(request): 
     context={} 
     # user=request.user
     # user_profile=User.objects.filter(id=user.id)
     user_one = ProfilePageModel.objects.all()
     user_name=request.GET.get('id')
     usernameprofile=None
     if user_name:
         usernameprofile=ProfilePageModel.objects.filter(user_id=request.user.id).first()
     context['usernameprofile']=usernameprofile
     context['user_one']=user_one
     context['user']=request.user
     return render(request,'profilepage.html',context)


def SaveProfile(request):
     status="OK"
     message="SUCCESS"
     payload={}
     
     user=request.user
     JobPostion=request.POST.get('JobPostion')
     file=request.FILES['file']
     dateofbirth= request.POST.get('dateofbirth')
     user_name=request.POST.get('user_name')
     
     try:
         log.debug("Profile image: %s", file)
         mediaPrefix = ("%s/%s") % (date.today().year, date.today().month)
         mediaPathDirectory = ("%s/%s") % (settings.MEDIA_ROOT, mediaPrefix)
         if not os.path.exists(mediaPathDirectory):
             os.makedirs(mediaPathDirectory)
         extension = file.name.split(u'.')[-1]
         new_filename = "profile-pic-%s.%s" % (random.randint(0, 10000), extension)
         path = os.path.join(mediaPathDirectory, new_filename)
         dest = open(path, 'wb+')
         for chunk in file.chunks():
             dest.write(chunk)
             dest.close()
         image_url = "%s/%s" % (mediaPrefix, new_filename)
         
         if user_name:
             userprofile=ProfilePageModel.objects.filter(user_id=user.id).first()
             if userprofile:
                 userprofile.jobposition= JobPostion
                 userprofile.profilepic= image_url 
                 userprofile.dateOfBirth= dateofbirth
                 userprofile.save()
                 log.debug("Saved profile image successfully for user: %s", request.user.id)
                 
         else:
             ProfilePageModel.objects.create(user_id=user.id,jobposition=JobPostion,profilepic=image_url,dateOfBirth=dateofbirth)
             log.debug("user profile not found, creating a new one")
     except:
         status = "FAIL"
         message = "SYSTEM_ERROR" 
         log.error("Error while saving description name", exc_info=1) 
     response = {"status": status, "message": message, "payload": payload}   
     return HttpResponse(json.dumps(response)) 
 
def signed_up(request):
     context={}
     return render(request,'verifiedsignup.html',context)  
    
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
     try:
         if description and datetime_from and datetime_to and  Duration:
             status='OK'
             payload={}
             message='SUCCESS'
        
             if idUserVaca:
                 user_vaca=HomePageModel.objects.filter(id=idUserVaca).first()
                 if user_vaca:
                     user_vaca.description= description
                     user_vaca.datetimefrom= datetime_from
                     user_vaca.datetimeto= datetime_to
                     user_vaca.Duration= Duration
                     user_vaca.save()    
                     log.debug("%s vacation successfully" % ("Updated" if idUserVaca else "Created"))
                 else:
                     message="VACATION_NOT_FOUND"
             else:
                 HomePageModel.objects.create(user=user,description=description,datetimefrom=datetime_from,datetimeto=datetime_to,Duration=Duration)
         else:   
             message="MISSING_REQUIRED_PARAMETERS"
             status="FAIL"
     except:
         status = "FAIL"
         message = "SYSTEM_ERROR" 
         log.error("Error while saving Description name", exc_info=1)
       
     response={'status':status,'message':message,'payload':payload}
     return HttpResponse(json.dumps(response))

@login_required(login_url='LogIn/') 
def vacation_table(request):
     # user_info=HomePageModel.objects.all()
     # context={"user_info":user_info,"present_user":request.user}  
     context={}
     return render(request,'vacationtable.html',context)
    

def vacation_grid(request): 
     data=[]
     table_length=request.POST.get('length')
    
     global_search=request.POST.get('search[value]')
     qset= Q(user_id=request.user.id)
     
     sorting_column= request.POST.get("order[0][column]")
     sorting_column_type=request.POST.get("order[0][dir]")
     
     sorted_column=request.POST.get('columns[%s][name]' % (sorting_column))

     if global_search:
         qset &= Q(description__icontains=global_search)
     
     description_search=request.POST.get('columns[0][search][value]')
     if  description_search:
         qset &=Q(description__icontains=description_search)
         
     datetimefrom_search=request.POST.get('columns[1][search][value]')
     if  datetimefrom_search:
         qset &=Q(datetimefrom__exact=datetimefrom_search)
     
     datetimeto_search=request.POST.get('columns[2][search][value]')
     if  datetimeto_search:
         qset &=Q(datetimeto__exact=datetimeto_search)
         
     Duration_search=request.POST.get('columns[3][search][value]')
     if  Duration_search:
         qset &=Q(Duration__exact=Duration_search)
    
     user_info=HomePageModel.objects.filter(qset).all().order_by('%s%s' %("-" if sorting_column_type=="desc" else "" ,sorted_column))[:int(table_length)]
     
     for info in user_info:
         data.append({'id':info.id,'description':info.description,'datetimefrom':info.datetimefrom,'datetimeto':info.datetimeto,'Duration':info.Duration,'status': "Active" if info.status else "Not Active"})
         
         
     records=len(user_info)
     response={
         'draw': request.POST.get('draw'),
         'recordsTotal':records,
         'recordsFiltered':records,
         'data':data,
         
    }
     return HttpResponse(json.dumps(response,sort_keys=True,indent=1,cls=DjangoJSONEncoder))
def update_status(request):
     vacation_id=request.POST.get('vacation_Id')
    
     try:
         status='OK'
         payload={}
         message='SUCCESS'
    
         if vacation_id:
             user_vaca=HomePageModel.objects.filter(id=vacation_id).first()
             
             vacation_status=user_vaca.status
             
             user_vaca.status= not vacation_status
             user_vaca.save()   
            
         else:
             message="VACATION_NOT_FOUND"
     except:
         message="MISSING_REQUIRED_PARAMETERS"
         status="FAIL"
       
     response={'status':status,'message':message,'payload':payload}
     
     return HttpResponse(json.dumps(response))
def delete_vacation(request):
     vacation_id = request.POST.get('vacation_id')

     try:

         status = "OK"
         message = "SUCCESS"
         payload = {}
     
         if vacation_id:
             vacation = HomePageModel.objects.filter(id=vacation_id).first()
             vacation.delete()
           
         else:
             message = "VACATION_NOT_FOUND"
             status = "FAIL"
            
     except:
         message = "SYSTEM_ERROR"
         status = "FAIL"
        
     response = {'status': status, 'message': message, 'payload': payload}
    
     return HttpResponse(json.dumps(response))
    
def logOutUser(request):
     logout(request)
     return HttpResponseRedirect(reverse('userLogin'))
def base_Page(request):
     context={"user":request.user}
     render(request,'base.html',context)
     
urlpatterns = [
    
     url(r'register/',register,name="register"),
     url(r'LogIn/',userLogin,name="userLogin"),
     url(r'ProfilePageView/',ProfilePageView,name="ProfilePageView"),
     url(r'HomePage/',HomePageView,name="HomePageView"),
     url(r'vacation_table/',vacation_table,name="vacation_table"),
     url(r'savedPage/',savedHomePage,name="savedHomePage"),
     url(r'mainPage',mainPage,name="mainPage"),
     url(r'logOut/',logOutUser,name="logOutUser"),
     url(r'base_Page/',base_Page,name="base_Page"),
     url(r'signed_up/',signed_up,name="signed_up"),
     url(r'SaveProfile/',SaveProfile,name="SaveProfile"),
     url(r'vacation_grid/',vacation_grid,name="vacation_grid"),
     url(r'update_status/',update_status,name="update_status"),
     url(r'delete_vacation/',delete_vacation,name="delete_vacation"),
    ]