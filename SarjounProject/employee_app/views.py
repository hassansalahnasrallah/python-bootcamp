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
import logging
from SarjounProject import settings
from _datetime import date, datetime
import os
import random
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder
# Create your views here.

log = logging.getLogger(__name__)

def Login(request):
    try:
        context={}
        if request.method == 'POST':
             username = request.POST.get('username')
             password = request.POST.get('password')
             user = authenticate(username=username, password=password)
             if user:
                  if user.is_active:
                     login(request, user)
                     log.debug("Welcome ")
                     return HttpResponseRedirect(reverse('vacation_table'))
                  else:
                      return HttpResponse("Your account is not active.")
             else:
                 log.debug("Someone tried to login and failed.")
                 log.debug("They used username: {} and password: {}".format(username,password))
                 return HttpResponse("Invalid login details supplied.")
    except:
        log.debug("Error while logIn")
    return render(request,'login.html',context)


def Signup(request):
    """
    Signup form
    """
    try:
        signup_form = forms.FormSignup()
        if request.method=='POST':
            signup_form=forms.FormSignup(data=request.POST)
            
            if signup_form.is_valid:
                user=signup_form.save()
                user.set_password(user.password)
                user.save()
                log.debug("You have  registered successfully " )
                login(request, user)
                return HttpResponseRedirect(reverse('vacation_table'))
    except:  
        log.debug("Error while registering")
    
    context={'signup_form':signup_form}

    return render(request,'signup.html',context)
@login_required
def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

@login_required()
def vacation_table(request):
    context={}
    return render(request,'vacation_table.html',context)

def vacation_grid(request):
    """
    Display grid of vacation
    """
    
    #response=[{'title':"vacation title"}]
    
    data = []
    table_length = request.POST.get('length')
    global_search =request.POST.get('search[value]')
    sorting_column_index = request.POST.get('order[0][column]')
    sorting_column_direction = request.POST.get('order[0][dir]')
    sorted_column = request.POST.get('columns[%s][name]' % (sorting_column_index))
    qset = Q(user_id=request.user.id)
    
    description_search=request.POST.get('columns[0][search][value]')
    if description_search:
        qset &= Q(Description__icontains=description_search)
    datefrom_search=request.POST.get('columns[1][search][value]')
    
    if datefrom_search:
        qset &= Q(Datetime_From__icontains=datefrom_search) 
    dateto_search=request.POST.get('columns[2][search][value]')
    
    if dateto_search:
        qset &= Q(Datetime_To__icontains=dateto_search) 
    duration_search=request.POST.get('columns[3][search][value]')
    
    if duration_search:
        qset &= Q(Duration__icontains=duration_search)
        
    vacations = Vacation.objects.filter(qset).all().order_by("%s%s" % ("-" if sorting_column_direction == "desc" else "", sorted_column))[:int(table_length)]
    log.debug("Total retrieved: %s", len(vacations))
    
    
    for vacation in vacations:
        data.append({'id': vacation.id,  'description': vacation.description, 'duration': vacation.duration,
                     'status': "Active" if vacation.status else "Not active", 'datefrom': datetime.strftime(vacation.datefrom, '%d/%m/%Y'), 'dateto': datetime.strftime(vacation.dateto, '%d/%m/%Y')})
    
    
    records = len(vacations)
    
    response = {
        'recordsTotal': records,
        'recordsTotal': records,
        'data': data,
        
        }
    
    return HttpResponse(json.dumps(response,sort_keys=True,indent=1,cls=DjangoJSONEncoder))

def update_status(request):
    """
    Update status
    """
    vacation_id = request.POST.get('vacation_id')

    status = "OK"
    message = "SUCCESS"
    payload = {}
    
    try:
        if vacation_id:
            #update
            vacation = Vacation.objects.filter(id=vacation_id).first()
            vacation_status = vacation.status
            log.debug(vacation_status)
            vacation.status = not vacation_status
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
    """
    Delete vacation
    """
    vacation_id = request.POST.get('vacation_id')

    status = "OK"
    message = "SUCCESS"
    payload = {}
    
    try:
        if vacation_id:
            #update
            vacation = Vacation.objects.filter(id=vacation_id).first()
            
            vacation.delete()
                
            response = "SUCCESS"
            
            log.debug(" vacation is deleted successfully")
        else:
            message = "VACATION_NOT_FOUND"
            status = "FAIL"
            
    except:
        message = "SYSTEM_ERROR"
        status = "FAIL"
        log.error("Error while deleting vacation", exc_info=1)
                
    response = {'status': status, 'message': message, 'payload': payload}
    
    return HttpResponse(json.dumps(response))


@login_required()
def Add_Vacation(request):
    """
    Here Employees Add their Vacations 
    """
    context={}
    log.debug("Now we can add a vacation")
    vacation_id=request.GET.get('id')
    vacation=None
    if vacation_id:
        vacation=Vacation.objects.filter(id=vacation_id).first()
    context['vacation']=vacation
    return render(request,'Add_Vacation.html',context)

def save_vacation(request):
    """
    Update add vacation for logged in user
    """
    description = request.POST.get('desc')
    datefrom = request.POST.get('date_from')
    dateto = request.POST.get('date_to')
    duration = request.POST.get('duration')
    vacation_id = request.POST.get('vacation_id')

    status = "OK"
    message = "SUCCESS"
    payload = {}
    
    try:
        if description and datefrom and dateto and duration: 
            if vacation_id:
                #update
                vacation = Vacation.objects.filter(id=vacation_id).first()
                if vacation:
                    vacation.description = description
                    vacation.datefrom = datetime.strptime(datefrom, "%d/%m/%Y")
                    vacation.dateto = datetime.strptime(dateto, "%d/%m/%Y")
                    vacation.duration = duration
                    vacation.save()
                    
                    payload['id'] = vacation.id
                    response = "SUCCESS"
                    
                    log.debug("%s vacation successfully" % ("Updated" if vacation_id else "Created"))
                else:
                    message = "VACATION_NOT_FOUND"
                    status = "FAIL"
            else:
                 Employee_Vacation.objects.create(user=user,description=description,datefrom=datefrom,datetoo=dateto,duration=duration)
                 payload['id'] = vacation.id
                    
        else:
            message = "MISSING_REQUIRED_PARAMETERS"
            status = "FAIL"
    
    except IntegrityError:
        status = "FAIL"
        message = "DESCRIPTION_NAME_ALREADY_EXISTS"

    except:
        message = "SYSTEM_ERROR"
        status = "FAIL"
        log.error("Error while saving vacation", exc_info=1)
                
    response = {'status': status, 'message': message, 'payload': payload}
    
    return HttpResponse(json.dumps(response))

@login_required()
def EditProfile(request):
    context = {}
    
    context['MEDIA_URL'] = settings.MEDIA_URL
    context['user_profile'] = UserProfile.objects.filter(user_id=request.user.id).first()
    
    return render(request, "EditProfile.html", context)

def save_profile(request):
    status = "OK"
    message = "SUCCESS"
    payload = {}
    
    job_position = request.POST.get('jobposition')
    date_of_birth= request.POST.get('dateofbirth')
    profile_picture = request.FILES['profilepic']
    
    try:
        log.debug("Profile Picture: %s", profile_picture)  
        
        #define media prefix
        mediaPrefix = ("%s/%s") % (date.today().year, date.today().month)
        #define mediapath directory
        mediaPathDirectory = ("%s/%s") % (settings.MEDIA_ROOT, mediaPrefix)
        
        #check if path exists
        if not os.path.exists(mediaPathDirectory):
            # create media path dir if not found
            os.makedirs(mediaPathDirectory)
        
        #check image extension
        extension = profile_picture.name.split(u'.')[-1]  
        
        #rename profile image
        new_filename = "profile-pic-%s.%s" % (random.randint(0, 10000), extension)
        
        #set path
        path = os.path.join(mediaPathDirectory, new_filename)
        dest = open(path, 'wb+')
        
        #write image into dest
        #chunk means to read file peace by peace
        for chunk in profile_picture.chunks():
            dest.write(chunk)
            dest.close()
            
        image_url = "%s/%s" % (mediaPrefix, new_filename)
        
        user_profile = UserProfile.objects.filter(user_id=request.user.id).first()
        if not user_profile:
            user_profile = UserProfile.objects.create(user_id=request.user.id)
            log.debug("user profile not found, creating a new one")
        
        user_profile.profile_picture = image_url
        user_profile.job_position=job_position
        user_profile.date_of_birth=date_of_birth
        user_profile.save()
        log.debug("Saved profile image successfully for user: %s", request.user.id)
        payload['image_url'] = image_url
        
    except:
        status = "FAIL"
        message = "SYSTEM_ERROR" 
        log.error("Error while saving topic name", exc_info=1)
    
    response = {"status": status, "message": message, "payload": payload}
    
    return HttpResponse(json.dumps(response))


urlpatterns=[
    url(r'login',Login,name='login'),
    url(r'logout/',Logout , name ='logout'),
    url(r'signup/', Signup ,name ='sign_up'),
    url(r'vacation_table/', vacation_table, name='vacation_table'),
    url(r'Add_Vacation', Add_Vacation, name ='Add_Vacation'),
    url(r'vacation_grid', vacation_grid, name ='vacation_grid'),
    url(r"save_vacation/", save_vacation ,name ="save_vacation"),
    url(r"EditProfile/", EditProfile ,name ="EditProfile"),
    url(r"save_profile/", save_profile ,name ="save_profile"),
    url(r"update_status/", update_status ,name ="update_status"),
    url(r"vacation_delete", save_profile ,name ="delete_vacation"),
    ]