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
from _datetime import date
import os
import random
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder
# Create your views here.

log = logging.getLogger(__name__)

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
                return HttpResponseRedirect(reverse('vacation_table'))
            else:
                return HttpResponse("Not connected")
        else:
            return HttpResponse("User not found")
    else:
         return render(request,'login.html', context)
    
    return render(request,'login.html',context)


def Signup(request):
    """
    
    """
   # userprofileinfo=forms.UserInfo()
    signup_form = forms.FormSignup()
    sign_up = False
    
    if request.method=='POST':
        signup_form=forms.FormSignup(data=request.POST)
        #userprofileinfo=forms.UserInfo(data=request.POST)
        
        if signup_form.is_valid:
            user=signup_form.save()
            user.set_password(user.password)
            user.save()
            # profile=userprofileinfo.save(commit=False)
            # profile.user=user
            # profile.save()
            sign_up=True
            login(request,user)
            return HttpResponseRedirect(reverse('vacation_table'))
        else:
            #User logging
            print("User not found")
    else:
        print("Not valid")

    context={'signup_form':signup_form, 'sign_up':sign_up}

    return render(request,'signup.html',context)
@login_required
def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

@login_required()
def vacation_table(request):
    context={}
    return render(request,'vacation_table.html',context)


@login_required()
def Add_Vacation(request):
    context={}
    vacation_id=request.GET.get('id')
    vacation=None
    if vacation_id:
        vacation=Vacation.objects.filter(id=vacation_id).first()
    context['vacation']=vacation
    return render(request,'Add_Vacation.html',context)

def vacation_grid(request):
    
    
    response = [{'title': "vacation title"}, ]
    
    data = []
    user_id = request.POST.get('user_id')
    all_vacations = Vacation.objects.all()
    for vacation in all_vacations:
        data.append({'description': vacation.description,'datefrom': vacation.datefrom,'dateto': vacation.dateto})
    
    
    table_length = request.POST.get('length')
    global_search = request.POST.get('search[value]')
    
    sorting_column_index = request.POST.get('order[0][column]')
    sorting_column_direction = request.POST.get('order[0][dir]')
    
    sorted_column = request.POST.get('columns[%s][name]' % (sorting_column_index))
    
    qset = Q(user_id=user_id)
    
    if global_search:
        qset &= Q(description__icontains=global_search) | Q(datefrom__icontains=global_search) | Q(dateto__icontains=global_search)
        
    all_vacations = Vacation.objects.filter(qset).all().order_by("%s%s" % ("-" if sorting_column_direction == "desc" else "", sorted_column))[:int(table_length)]
    
    log.debug("Total retrieved: %s", len(all_vacations))
    
    for vacation in all_vacations:
        data.append({'id': vacation.id, 'description': vacation.description, 'datefrom': vacation.datefrom, 'dateto': vacation.dateto})
        
    
    records = len(all_vacations)
    
    response = {
        #'draw': request.GET.get("_"),
        'recordsTotal': records,
        'recordsFiltered': records,
        'data': data,
    }
    
    return HttpResponse(json.dumps(response,sort_keys=True,indent=1,cls=DjangoJSONEncoder))


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
    return HttpResponseRedirect(reverse('vacation_table'))

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
    
    profile_picture = request.FILES['profilepic']
    job_position = request.POST.get('jobposition')
    date_of_birth= request.POST.get('dateofbirth')
    
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
        
    except:
        status = "FAIL"
        message = "SYSTEM_ERROR" 
        log.error("Error while saving topic name", exc_info=1)
    
    response = {"status": status, "message": message, "payload": payload}
    
    return HttpResponse(json.dumps(response))


urlpatterns=[
    url(r'login/',Login,name='login'),
    url(r'logout/',Logout , name ='logout'),
    url(r'signup/', Signup ,name ='sign_up'),
    url(r'vacation_table/', vacation_table, name='vacation_table'),
    url(r'Add_Vacation', Add_Vacation, name ='Add_Vacation'),
    url(r'vacation_grid', vacation_grid, name ='vacation_grid'),
    url(r"save/", save ,name ="save"),
    url(r"EditProfile/", EditProfile ,name ="EditProfile"),
    url(r"save_profile/", save_profile ,name ="save_profile"),
    ]