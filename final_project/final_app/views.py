from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.conf.urls import url
from . import forms
from django.contrib.auth import authenticate, login , logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from final_app.models import Vacation, UserProfile
import json

from django.db.utils import IntegrityError
from final_project import settings
import logging
from datetime import date, datetime
import os
import random
from django.db.models import Q 

log = logging.getLogger(__name__)

# Create your views here.

def index(request):
    """
    Main Page
    """
    context = {}

    log.debug("Now we are in the Home page")
    
    context['MEDIA_URL'] = settings.MEDIA_URL
    context['user_profile'] = UserProfile.objects.filter(user_id=request.user.id).first()
    return render(request, 'index.html', context)

def test(request):
    context = {}
    return render(request, 'test.html', context)


def register(request):
    """
    Register for a new user
    
    """
    log.debug("Now we are in the Registration form")
    context = {}

    context['MEDIA_URL'] = settings.MEDIA_URL
    context['user_profile'] = UserProfile.objects.filter(user_id=request.user.id).first()
    return render(request,'registration.html',context)

def registration_save(request):
    """
    Save and update the registration form
    """
    
    status = "OK"
    message = "SUCCESS"
    payload = {}
    
    log.debug("request.FILES: %s",request.FILES)
    
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    position = request.POST.get('position')
    date_of_birth = request.POST.get('date_of_birth')
    profile_img = request.FILES.get('profile_img')
    register_id = request.POST.get('register_id')
    
    try:
        log.debug("Profile image: %s",profile_img)
        
        mediaPrefix = ("%s/%s")%(date.today().year, date.today().month)
        mediaPathDirectory = ("%s/%s") % (settings.MEDIA_ROOT, mediaPrefix)
        
        if not os.path.exists(mediaPathDirectory):
            os.makedirs(mediaPathDirectory)
            
        extension = profile_img.name.split(u'.')[-1]  
         
        new_filename = "profile-pic-%s.%s"%(random.randint(0, 10000), extension)
        
        path = os.path.join(mediaPathDirectory, new_filename)
        dest = open(path, 'wb+')
        
        for chunk in profile_img.chunks():
            dest.write(chunk)
            dest.close()
            
        image_url = "%s/%s"%(mediaPrefix, new_filename)
        
        
        
        
        if username and email and password and first_name and last_name and position and date_of_birth and profile_img:
            
            if register_id:
              
                user_profile = UserProfile.objects.filter(user_id = request.user.id).first()
            else:
                user_profile = UserProfile(user_id=request.user.id)
            
            
            
            if user_profile:
                user_profile.username = username
                user_profile.email = email
                user_profile.password = password
                user_profile.first_name = first_name
                user_profile.last_name = last_name  
                user_profile.picture = image_url
                user_profile.position = position
                user_profile.date_of_birth = datetime.strptime(date_of_birth, "%d/%m/%Y")

        
                user_profile.save()
                
                payload['id'] = user_profile.id
                response = "SUCCESS"
                
                log.debug('successfully registered for user %s', request.user.id)
            else:
                message = "USER_NOT_FOUND"
                status = "FAIL"
                
        else:
            message = "MISSING_REQUIRED_PARAMETERS"
            status = "FAIL" 
        
        payload['image_url'] = image_url
    
    except:
 
        message = "SYSTEM_ERROR"
        status = "FAIL"
        log.error("Error while saving registration form", exc_info=1)
                  
    
    response = {'status': status, 'message': message, 'payload': payload }
     
    return HttpResponse(json.dumps(response))

"""
def register(request):   
    
    Register to the app 
    
    #TODO add try catch and logging
    user_form = forms.UserForm
    profile_form = forms.UserProfileInfoForm
    
    registered = False
    
    if request.method == "POST":
        
        user_form = forms.UserForm(data=request.POST)
        profile_form = forms.UserProfileInfoForm(data = request.POST)
        #date_of_birth = request.POST.get('date_of_birth')
        
        
        if user_form.is_valid() and profile_form.is_valid():
            
            print("form valid")
            #save data
            user = user_form.save()
            user.set_password(user.password)
            
            user.save()
            
            profile = profile_form.save(commit=False)
            #commit=false prevent to save the profile bbecause still need to edit profile (bdna User)
            
            profile.user=user
            #profile.date_of_birth = datetime.strptime(date_of_birth, "%d/%m/%Y")
            #check if profile pic provided
            if 'picture' in request.FILES:
                print("found the picture")
                profile.picture = request.FILES['picture']
                
            
            
            profile.save()
            log.debug("Saved profile and user for user: %s", user)
            registered = True
            #login user
            login(request,user)
            #redirect to the home or vacation page
            return HttpResponseRedirect(reverse('vacation_page'))
            
        else:
            print("form not valid")
            
    else:
        print("Not valid request")  
              
    context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered}
    
    return render(request,'registration.html',context)
"""




def user_login(request):
    """
    log in into the app
    """
    
    context={}
    
    if request.method == 'POST':
        username=request.POST.get('username') 
        password=request.POST.get('password')
        
        loggedin = False
        
        
        
        user = authenticate(username=username,password=password)
        
        
        if user:
            
            if user.is_active:
                login(request, user)
                
                loggedin = True
                
                return HttpResponseRedirect( reverse('vacation_page'))


            
            else:
                return HttpResponse("Your account is not active") 
            
        else:
            return render (request,'invalid_login.html',context)
                  
    else:
        return render (request,'login.html',context)
        
    context = {'loggedin': loggedin}
    
    return render (request,'login.html',context)

def user_logout(request):
    logout(request)

    return HttpResponseRedirect(reverse('index'))           


@login_required
def vacation_page(request):
    """
    
    """
    
    context = {}
    
    context['vacations'] = [{'id': v.id, 'title': v.description, 'start': datetime.strftime(v.date_from,'%Y-%m-%d'), 'end':  datetime.strftime(v.date_to,'%Y-%m-%d')} for v in Vacation.objects.filter(employee_id=request.user.id).all()]
    
    return render (request,'vacation_page.html',context)

@login_required
def vacation_form(request):
    """
    Show vacation form for the logged in user 
    """
    
    log.debug("Now we are in the vacation form")
    context = {}
    
    vacation_id = request.GET.get('id')
    employee_vacation = None
    if vacation_id:
        employee_vacation = Vacation.objects.filter(id=vacation_id).first()
        print("there is a vacation id")
        
    context['MEDIA_URL'] = settings.MEDIA_URL
    context['user_profile'] = UserProfile.objects.filter(user_id=request.user.id).first()
    context['vacation'] = employee_vacation
    
    return render(request,'vacation_form.html',context)


@login_required
def save_vacation(request):     
    """
    Update add vacation for logged in user
    """
    description = request.POST.get('description')
    date_from = request.POST.get('date_from')
    date_to = request.POST.get('date_to')
    duration = request.POST.get('duration')
    vacation_id = request.POST.get('vacation_id')

    status = "OK"
    message = "SUCCESS"
    payload = {}
    
    try:
        if description and date_from and date_to and duration: 
        
            if vacation_id:
                #update
                vacation = Vacation.objects.filter(id=vacation_id).first()
            else:
                vacation = Vacation(employee_id=request.user.id)
            
            if vacation:
                vacation.description = description
                vacation.date_from = datetime.strptime(date_from, "%d/%m/%Y")
                vacation.date_to = datetime.strptime(date_to, "%d/%m/%Y")
                vacation.duration = duration
                vacation.save()
                
                payload['id'] = vacation.id
                response = "SUCCESS"
                
                log.debug("%s vacation successfully" % ("Updated" if vacation_id else "Created"))
            else:
                message = "VACATION_NOT_FOUND"
                status = "FAIL"
                
        else:
            message = "MISSING_REQUIRED_PARAMETERS"
            status = "FAIL"

    except:
        message = "SYSTEM_ERROR"
        status = "FAIL"
        log.error("Error while saving vacation", exc_info=1)
                
    response = {'status': status, 'message': message, 'payload': payload}
    
    return HttpResponse(json.dumps(response))


@login_required
def vacation_grid(request):
    """
    Display grid of vacation
    """
    
    #response=[{'title':"vacation title"}]
    log.debug("Now we are in the vacation table")
    data = []
    
    employee_id = request.user.id #request.POST.get('employee_id')
    table_length = request.POST.get('length')
    global_search =request.POST.get('search[value]')
    
    
    sorting_column_index = request.POST.get('order[0][column]')
    sorting_column_direction = request.POST.get('order[0][dir]')
    
    sorted_column = request.POST.get('columns[%s][name]' % (sorting_column_index))
    
    qset = Q(employee_id=employee_id)
    
    if global_search:
        qset &= Q(description__icontains=global_search)
        
    description_search = request.POST.get('columns[1][search][value]')
    if description_search:
        qset &= Q(description__icontains=description_search)
        
    duration_search = request.POST.get('columns[4][search][value]')
    if duration_search:
        qset &= Q(duration__contains=duration_search)    
           
        
        
    
    
    vacations = Vacation.objects.filter(qset).all().order_by("%s%s" % ("-" if sorting_column_direction == "desc" else "", sorted_column))[:int(table_length)]
    log.debug("Total retrieved objects: %s", len(vacations))
    
    
    for vacation in vacations:
        data.append({'id': vacation.id,  'description': vacation.description, 'duration': vacation.duration,
                     'status': "Active" if vacation.status else "Not active", 'date_from': datetime.strftime(vacation.date_from, '%d/%m/%Y'), 'date_to': datetime.strftime(vacation.date_to, '%d/%m/%Y')})
    
    
    records = len(vacations)
    
    response = {
        'recordsTotal': records,
        'recordsFiltered': records,
        'data': data,
        }
    
    return HttpResponse(json.dumps(response))

def profile_form(request):
    """
    Display the profile form
    """
    log.debug("Now we are in the Profile form")
    context = {}

    context['MEDIA_URL'] = settings.MEDIA_URL
    context['user_profile'] = UserProfile.objects.filter(user_id=request.user.id).first()
    return render(request,'profile_form.html',context)

def save_profile(request):
    """
    Save and update the profile form
    """
    
    status = "OK"
    message = "SUCCESS"
    payload = {}
    
    log.debug("request.FILES: %s",request.FILES)
    profile_img = request.FILES.get('profile_img')
    position = request.POST.get('position')
    date_of_birth = request.POST.get('date_of_birth')
    try:
        log.debug("Profile image: %s",profile_img)
        
        mediaPrefix = ("%s/%s")%(date.today().year, date.today().month)
        mediaPathDirectory = ("%s/%s") % (settings.MEDIA_ROOT, mediaPrefix)
        
        if not os.path.exists(mediaPathDirectory):
            os.makedirs(mediaPathDirectory)
            
        extension = profile_img.name.split(u'.')[-1]  
         
        new_filename = "profile-pic-%s.%s"%(random.randint(0, 10000), extension)
        
        path = os.path.join(mediaPathDirectory, new_filename)
        dest = open(path, 'wb+')
        
        for chunk in profile_img.chunks():
            dest.write(chunk)
            dest.close()
            
        image_url = "%s/%s"%(mediaPrefix, new_filename)
        
        
        user_profile = UserProfile.objects.filter(user_id = request.user.id).first()
        
        if not user_profile:
            user_profile = UserProfile.objects.create(user_id = request.user.id)  
            log.debug("user profile not found creating a new one")
            
        user_profile.picture = image_url
        user_profile.position = position
        user_profile.date_of_birth = datetime.strptime(date_of_birth, "%d/%m/%Y")

        
        user_profile.save()
        log.debug('Saved profile image successfully for user %s', request.user.id)
        
        payload['image_url'] = image_url
    except:
 
        message = "SYSTEM_ERROR"
        status = "FAIL"
        log.error("Error while saving profile form", exc_info=1)
                  
    
    response = {'status': status, 'message': message, 'payload': payload }
     
    return HttpResponse(json.dumps(response))


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
            
            vacation.status = not vacation_status
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
          
            vacation = Vacation.objects.filter(id=vacation_id).first()
            
            vacation.delete()
                
            response = "SUCCESS"
            
            log.debug("vacation successfully deleted")
        else:
            message = "VACATION_NOT_FOUND"
            status = "FAIL"
            
    except:
        message = "SYSTEM_ERROR"
        status = "FAIL"
        log.error("Error while deleting vacation", exc_info=1)
                
    response = {'status': status, 'message': message, 'payload': payload}
    
    return HttpResponse(json.dumps(response))


def vacation_details(request):
    """
    Display the subgrid datatable
    """
    vacation_id = request.GET.get('vacation_id')
    
    log.debug("Now we are in the vacation details html")
    context = {}

    
    context['vacation_details'] = Vacation.objects.filter(id=vacation_id).first()
    return render(request,'vacation_details.html',context)



urlpatterns = [
  url(r'^$',index,name="index"),
  url(r'test/',test,name="test"),
  url(r'register/',register,name="register"),
  url(r'registration_save/',registration_save,name="registration_save"),
  url(r'user_login/',user_login,name="user_login"),
  url(r'user_logout/',user_logout,name="user_logout"), 
  url(r'table/',vacation_page,name="vacation_page"),
  url(r'vacation/',vacation_form,name="vacation_form"),
  url(r'vacation_save/',save_vacation,name="save_vacation"), 
  url(r'vacation_grid/',vacation_grid,name="vacation_grid"),
  url(r'profile/',profile_form,name="profile_form"),
  url(r'save_profile_user/',save_profile,name="save_profile"),
  url(r'update_status/',update_status,name="update_status"),
  url(r'delete/',delete_vacation,name="delete_vacation"),
  url(r'details/',vacation_details,name="vacation_details"),

    ]
