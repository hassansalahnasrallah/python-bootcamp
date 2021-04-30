from django.shortcuts import render
from django.http.response import HttpResponse,HttpResponseRedirect
from django.conf.urls import url
from employee_app import forms
from django.template.context_processors import request
from django.contrib.auth import authenticate,login, logout
from django.urls.base import reverse
from django.contrib.auth.decorators import login_required
from employee_app.models import Employee_Vacation,Employee_Profile 
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
import os
import random
import logging
from employee_project import settings
from django.db.utils import IntegrityError
import json
from datetime import date ,datetime
from django.db.models import Q
from django.http import response


# Create your views here.

log = logging.getLogger(__name__)


def sign_up_form(request):
    try:
        userinfo = forms.UserForm()
        if request.method == 'POST':
            userinfo = forms.UserForm(data=request.POST)
            if  userinfo.is_valid() :
                user = userinfo.save()
                user.set_password(user.password)
                user.save()
                log.debug("You have  registered successfully " )
                return HttpResponseRedirect(reverse('user_login'))
    except:  
        log.debug("Error while registering")
        
    context = {"user_form": userinfo}              
    return render(request,"employee_app/sign_up.html",context)    

def user_login(request):
    try:
        if request.method == 'POST':
             username = request.POST.get('username')
             password = request.POST.get('password')
             user = authenticate(username=username, password=password)
             if user:
                  if user.is_active:
                     login(request, user)
                     log.debug("Welcome You have LogIn ")
                     return HttpResponseRedirect(reverse('Vacation_Table'))
                  else:
                      return HttpResponse("Your account is not active.")
             else:
                 log.debug("Someone tried to login and failed.")
                 log.debug("They used username: {} and password: {}".format(username,password))
                 return HttpResponse("Invalid login details supplied.")
    except:
        log.debug("Error while logIn")
        
    return render(request, 'employee_app/login.html', {})
    

@login_required
def vacation_fields(request):
        context = {}    
        log.debug("Now we are in the vacation field")
        vacation_id = request.GET.get('id')
        vacation = None
        if vacation_id:
            vacation = Employee_Vacation.objects.filter(id=vacation_id).first()
        context['vacation'] = vacation   
        return render(request,"employee_app/Vacation_requirments.html",context)
    
def vacation_save(request):
     user = request.user
     Description = request.POST.get("desc")
     Date_From = request.POST.get("datefrom")
     Date_To = request.POST.get("dateto")
     Duration = request.POST.get("duration_d")
     vacation_id = request.POST.get("vacation_id")
     status = "OK"
     message = "SUCCESS"
     payload = {}
     try:
         if Description and Date_From and Date_To and  Duration:
             if vacation_id:
                 vacation = Employee_Vacation.objects.filter(id=vacation_id).first()
                 if vacation:
                      vacation.Description = Description
                      vacation.Datetime_From = Date_From
                      vacation.Datetime_To = Date_To
                      vacation.Duration = Duration
                      vacation.save()
                      payload['id'] = vacation.id
                      response = "SUCCES"
                      log.debug("%s vacation successfully" % ("Updated" if vacation_id else "Created"))
                 else:
                      message = "Description_NOT_FOUND"
                      status = "FAIL"
             else:
                 Employee_Vacation.objects.create(user=user,Description=Description,Datetime_From=Date_From,Datetime_To=Date_To,Duration=Duration)
                 log.debug("vacation is created successfly")
         else:
             message = "MISSING_REQUIRED_PARAMETERS"
             status = "FAIL"
     except IntegrityError:
        status = "FAIL"
        message = "DESCRIPTION_NAME_ALREADY_EXISTS"
        
     except:
         status = "FAIL"
         message = "SYSTEM_ERROR" 
         log.error("Error while saving Description name", exc_info=1)
     response = {"status": status, "message": message, "payload": payload}    
     return HttpResponse(json.dumps(response))
     

     return render(request,"employee_app/Vacation_table.html",context)

@login_required
def vacation_table(request):
    context = {}
    context['vacations'] = [{'id': vacation.id, 'title': vacation.Description, 'start':datetime.strftime(vacation.Datetime_From,'%Y-%m-%d') , 'end': datetime.strftime(vacation.Datetime_To,'%Y-%m-%d')} for vacation in Employee_Vacation.objects.filter(user_id=request.user.id).all()]
    return render(request, "employee_app/Vacation_table.html", context)


def vacation_grid(request):
    data = []
   
    table_length = request.POST.get('length')
    global_search = request.POST.get('search[value]')
    sorting_column_index = request.POST.get('order[0][column]')
    sorting_column_direction = request.POST.get('order[0][dir]')
    sorted_column_name = request.POST.get('columns[%s][name]' % (sorting_column_index))
    qset = Q(user_id=request.user.id)

    description_search=request.POST.get('columns[1][search][value]')
    if description_search:
        qset &= Q(Description__icontains=description_search)
    datefrom_search=request.POST.get('columns[2][search][value]')
    if datefrom_search:
        qset &= Q(Datetime_From__icontains=datefrom_search) 
    dateto_search=request.POST.get('columns[3][search][value]')
    if dateto_search:
        qset &= Q(Datetime_To__icontains=dateto_search) 
    duration_search=request.POST.get('columns[4][search][value]')
    if duration_search:
        qset &= Q(Duration__icontains=duration_search) 
    
    all_vacations = Employee_Vacation.objects.filter(qset).all().order_by("%s%s" % ("-" if sorting_column_direction == "desc" else "", sorted_column_name))[:int(table_length)]
    log.debug("Total retrieved: %s", len(all_vacations))
    
    for vacation in all_vacations:
        data.append({ 'id': vacation.id, 'Description': vacation.Description, 'Datetime_From': vacation.Datetime_From, 'Datetime_To': vacation.Datetime_To,'Duration':vacation.Duration,  'status':"Active" if vacation.status else "Not active"})
         
    records = len(all_vacations) 
    response = {
        'recordsTotal': records,
        'recordsFiltered': records,
        'data': data,
        }
    return HttpResponse(json.dumps(response,sort_keys=True,indent=1,cls=DjangoJSONEncoder))
 
@login_required 
def profile_form(request):
    context = {}
    context['MEDIA_URL'] = settings.MEDIA_URL
    context['employee_profile'] =  Employee_Profile.objects.all()
    context ['user_profile'] =  Employee_Profile.objects.filter(user_id=request.user.id).first()
    return render(request, "employee_app/Profile_Page.html", context)

def save_profile(request):
    status = "OK"
    message = "SUCCESS"
    payload = {}
    Job_position = request.POST.get('Job_position')
    profile_img = request.FILES['profile_img']
    Birth_date = request.POST.get('Birth_date')
    
    try:
        log.debug("Profile image: %s", profile_img)
        mediaPrefix = ("%s/%s") % (date.today().year, date.today().month)
        mediaPathDirectory = ("%s/%s") % (settings.MEDIA_ROOT, mediaPrefix)
        if not os.path.exists(mediaPathDirectory):
            os.makedirs(mediaPathDirectory)
        extension = profile_img.name.split(u'.')[-1]
        new_filename = "profile-pic-%s.%s" % (random.randint(0, 10000),extension)
        path = os.path.join(mediaPathDirectory, new_filename)
        dest = open(path, 'wb+')
        for chunk in profile_img.chunks():
            dest.write(chunk)
            dest.close()
        image_url = "%s/%s" % (mediaPrefix, new_filename)
        log.debug(image_url)
        user_profile = Employee_Profile.objects.filter(user_id=request.user.id).first()
        if not user_profile:
            user_profile = Employee_Profile.objects.create(user_id=request.user.id,job_position = Job_position,employe_profile = image_url,birth_date =  Birth_date)
            log.debug("user profile not found, creating a new one")
        else:    
            user_profile.job_position = Job_position
            user_profile.employe_profile = image_url
            user_profile.birth_date = Birth_date
            user_profile.save()
            log.debug("Saved profile image successfully for user: %s", request.user.id)
            payload['image_url'] = image_url
        
    except:
        status = "FAIL"
        message = "SYSTEM_ERROR" 
        log.error("Error while saving description name", exc_info=1)
        
    response = {"status": status, "message": message, "payload": payload}
    return HttpResponse(json.dumps(response))
 

 
@login_required
def employee_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Home'))

def jquery(request):
    return render(request,"employee_app/jquery.html",{})


def home(request):
    return render(request,"employee_app/home.html" , {})

def update_status(request):

    vacation_id = request.POST.get('vacation_id')

    status = "OK"
    message = "SUCCESS"
    payload = {}
    
    try:
        if vacation_id:
            vacation = Employee_Vacation.objects.filter(id=vacation_id).first()
            vacation_status = vacation.status
            log.debug(vacation_status)
            vacation.status = not (vacation_status)
            log.debug(vacation.status)
            vacation.save()
            
            response = "SUCCESS"
            
            log.debug("%s vacation successfully" % ("Updated" if vacation_id else "Created"))
        else:
            message = "VACATION_NOT_FOUND"
            status = "FAIL"
            
    except:
        message = "SYSTEM_ERROR"
        status = "FAIL"
        log.error("Error while saving vacation", exc_info=1)
                
    response = {'status': status, 'message': message, 'payload': payload}
    
    return HttpResponse(json.dumps(response))

def delete_vacation(request):
    vacation_id = request.POST.get('vacation_id')

    status = "OK"
    message = "SUCCESS"
    payload = {}
    
    try:
        if vacation_id:
            vacation = Employee_Vacation.objects.filter(id=vacation_id).first()
            vacation.delete()
            response = "SUCCESS"
            
            log.debug(" vacation is deleted successfully")
        else:
            message = "VACATION_NOT_FOUND"
            status = "FAIL"
            
    except:
        message = "SYSTEM_ERROR"
        status = "FAIL"
        log.error("Error while saving vacation", exc_info=1)
                
    response = {'status': status, 'message': message, 'payload': payload}
    
    return HttpResponse(json.dumps(response))

def vacation_details(request):
    """
    Display the subgrid datatable
    """
    vacation_id = request.GET.get('id')
    
    log.debug("Now we are in the vacation details html")
    context = {}

    
    context['vacation_details'] =Employee_Vacation.objects.filter(id=vacation_id).first()
    return render(request,'employee_app/vacation_details.html',context)


urlpatterns=[
    url(r'Sign_up/',sign_up_form,name='Sign_Up_Form'),
    url(r'login/',user_login,name='user_login') ,
    url(r'Vacation_Fields/', vacation_fields,name='Vacation_Fields') ,
    url(r'Vacation_Table/', vacation_table,name='Vacation_Table') ,
    url(r'Vacation_save/', vacation_save,name='Vacation_save') ,
    url(r'Vacation_grid/', vacation_grid,name='vacation_grid') ,
    url(r"profile/", profile_form, name="profile_form"),
    url(r"save_profile_user/", save_profile, name="save_profile"),
    url(r'logout/',employee_logout,name='employee_logout'),
    url(r'jquery/',jquery,name='jquery'),
    url(r'Home/',home,name='Home'),
    url(r'update_status/',update_status,name='update_status'),
    url(r'delete_vacation/',delete_vacation,name='delete_vacation'),
    url(r'details/',vacation_details,name="vacation_details"),
    ]