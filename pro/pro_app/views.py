from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.conf.urls import url
from . import forms
from django.contrib.auth import authenticate, login , logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from pro_app.models import Vacation, UserProfile
import json
from django.db.utils import IntegrityError
from pro import settings
import logging
from datetime import date, datetime
import os
import random
from django.db.models import Q 

log = logging.getLogger(__name__)

"""from forms import FormName"""

# Create your views here.

def index(request):
    context = {}
    log.debug("Index")
    log.info("Index ")
    log.warning("warning")
    log.error("ll")
    return render(request, 'index.html', context)

def test(request):
    context = {}
    return render(request, 'test.html', context)





def register(request):   
   
    user_form = forms.UserForm
    profile_form = forms.UserProfileInfoForm
    
    registered = False
    
    if request.method == "POST":
        
        user_form = forms.UserForm(data=request.POST)
        profile_form = forms.UserProfileInfoForm(data = request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            
            print("form valid")
            
            user = user_form.save()
            user.set_password(user.password)
            
            user.save()
            
            profile = profile_form.save(commit=False)
           
            profile.user=user
            
        
            if 'picture' in request.FILES:
                print("found the picture")
                profile.picture = request.FILES['picture']
            
            
            profile.save()
            log.debug("Saved profile and user for user: %s", user)
            registered = True
            
            login(request,user)
            
            return HttpResponseRedirect(reverse('vacation_page'))
            
        else:
            print("form not valid")
            
    else:
        print("Not valid request")  
              
    context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered}
    
    return render(request,'registration.html',context)


def employee_login(request):
        
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
            return HttpResponse("Invalid login details")
                  
    else:
        return render (request,'login.html',context)
        
    context={'loggedin': loggedin}
    
    return render (request,'login.html',context)

def employee_logout(request):
    logout(request)

    return HttpResponseRedirect(reverse('employee_login'))           


@login_required
@login_required
def vacation_page(request):
    """
    
    """
    
    context = {}
    
    #context['django_topic_id'] = Topic.objects.filter(topic_name="django").first().id
    context['vacations'] = Vacation.objects.all()
    
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
        user_profile.date_of_birth = date_of_birth
        
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
            #update
            vacation = Vacation.objects.filter(id=vacation_id).first()
            
            vacation.delete()
                
            response = "SUCCESS"
            
            log.debug("%s vacation successfully deleted")
        else:
            message = "VACATION_NOT_FOUND"
            status = "FAIL"
            
    except:
        message = "SYSTEM_ERROR"
        status = "FAIL"
        log.error("Error while saving vacation", exc_info=1)
                
    response = {'status': status, 'message': message, 'payload': payload}
    
    return HttpResponse(json.dumps(response))



urlpatterns = [
    
  url(r'^$',index,name="index"),
  url(r'test/',test,name="test"),
  url(r'register/',register,name="register"),
  url(r'employee_login/', employee_login,name="employee_login"),
  url(r'employee_logout/',employee_logout,name="employee_logout"),   
  url(r'profile_form/',profile_form,name="profile_form"),
  url(r'update_status/',update_status,name="update_status"),
  url(r'delete_vacation/',delete_vacation,name="delete_vacation"),   
  url(r'update_status/',update_status,name="update_status"),
  url(r'page/',vacation_page,name="vacation_page"),
  url(r'vacation2/',vacation_form,name="vacation_form"),
  url(r'vacation_save/',save_vacation,name="save_vacation"), 
  url(r'vacation_grid/',vacation_grid,name="vacation_grid"),
  url(r'save_profile/',save_profile,name="save_profile"),

    ]
