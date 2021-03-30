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
from datetime import date
import os
import random
from django.db.models import Q 

log = logging.getLogger(__name__)

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

@login_required
def table(request):
    context = {}
    return render(request, 'table.html', context)

#@login_required
#def form_vacation(request):
#     form=forms.VacationForm()
#    
#    
#     if request.method == 'POST':
#           form=forms.VacationForm(request.POST)
#           
#           if form.is_valid():
#                form.save(commit=True)
#                return index(request)
#           else:
#                print("ERROR")
          
          
                    
                
#     context={'form':form} 
         
#     return render(request,'vacation.html',context) 

def register(request):   
    """
    """
    #TODO add try catch and logging
    user_form = forms.UserForm
    profile_form = forms.UserProfileInfoForm
    
    registered = False
    
    if request.method == "POST":
        
        user_form = forms.UserForm(data=request.POST)
        profile_form = forms.UserProfileInfoForm(data = request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            
            print("form valid")
            #save data
            user = user_form.save()
            user.set_password(user.password)
            
            user.save()
            
            profile = profile_form.save(commit=False)
            #commit=false prevent to save the profile bbecause still need to edit profile (bdna User)
            
            profile.user=user
            
            #check if profile pic provided
            if 'picture' in request.FILES:
                print("found the picture")
                profile.picture = request.FILES['picture']
            
            
            profile.save()
            log.debug("Saved profile and user for user: %s", user)
            registered = True
            #login user
            #redirect to the home or vacation page
        else:
            print("form not valid")
            
    else:
        print("Not valid request")  
              
    context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered}
    
    return render(request,'registration.html',context)


#def save_register(request):     
    
#    description = request.POST.get('')
#    description_id = request.POST.get('')

#    return HttpResponse(json.dumps(response))



def user_login(request):
    """
    """
    
    context={}
    
    if request.method == 'POST':
        username=request.POST.get('username') 
        password=request.POST.get('password')
        
        loggedin = False
        
        #django built in authentication
        
        user = authenticate(username=username,password=password)
        #check if username valid then if active
        
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

def user_logout(request):
    logout(request)

    return HttpResponseRedirect(reverse('user_login'))           

#tene method heyye vacation grid

@login_required
def vacation_page(request):
    
    context = {}
    
    #context['django_topic_id'] = Topic.objects.filter(topic_name="django").first().id
    context['vacations'] = Vacation.objects.all()
    
    return render (request,'vacation_page.html',context)

def vacation_form(request):
    
    log.debug("Now we are in the vacation form")
    context = {}
    
    vacation_id = request.GET.get('id')
    employee_vacation = None
    if vacation_id:
        employee_vacation = Vacation.objects.filter(id=vacation_id).first()
        print("there is a vacation id")
        
    
    context['desc'] = employee_vacation
    
    return render(request,'vacation_form.html',context)

def save_vacation(request):     
    
    description = request.POST.get('description')
    vacation_id = request.POST.get('description_id')
    #desc
    
    
    status = "OK"
    message = "SUCCESS"
    payload = {}
    
    try:
        if description: #and and and 
        
            if vacation_id:
                #update
                vacation = Vacation.objects.filter(id = description_id).first()
            else:
                vacation = Vacation(employee_id=request.user.id)
            
            if vacation:
                vacation.description = description
                vacation.save()
                payload['id'] = desc.id
                response = "SUCCESS"
            else:
                message = "DESCRIPTION_NOT_FOUND"
                status = "FAIL"
                
#             else:
#                 #create
#                 desc = Vacation.objects.create(description=description )
#                 payload['id'] = desc.id
        else:
            message = "MISSING_REQUIRED_PARAMETERS"
            status = "FAIL!"
            

    except:
        message = "SYSTEM_ERROR"
        status = "FAIL!!"
        log.error("Error while saving vacation", exc_info=1)
                
    response = {'status': status, 'message': message, 'payload': payload }
    
    return HttpResponse(json.dumps(response))

def vacation_grid(request):
    """
    Display grid of vacation
    """
    
    #response=[{'title':"vacation title"}]
    
    data = []
    
    employee_id =request.user.id #request.POST.get('employee_id')
    
    vacations = Vacation.objects.filter(employee_id=employee_id).all()
    
    for vacation in vacations:
        data.append({'id': vacation.id,  'description': vacation.description, 'duration': vacation.duration,'status':vacation.status})#eza aktar mn field bzeed commas
        #, 'date_from': vacation.date_from, 'date_to': vacation.date_to
    
    
    records = len(vacations)
    
    response = {
        'recordsTotal': records,
        'recordsTotal': records,
        'data': data,
        
        }
    
    return HttpResponse(json.dumps(response))

def profile_form(request):
    
    
    context = {}

    context['MEDIA_URL'] = settings.MEDIA_URL
    context['user_profile'] = UserProfile.objects.filter(user_id=request.user.id).first()
    return render(request,'profile_form.html',context)

def save_profile(request):
    
    status = "OK"
    message = "SUCCESS"
    payload = {}
    
    log.debug("request.FILES: %s",request.FILES)
    profile_img = request.FILES['profile_img']
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
            dest.write(chunck)
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
        
    except:
 
        message = "SYSTEM_ERROR"
        status = "FAIL!!"
        log.error("Error while saving profile form", exc_info=1)
                  
    
    response = {'status': status, 'message': message, 'payload': payload }
     
    return HttpResponse(json.dumps(response))

urlpatterns = [
  url(r'^$',index,name="index"),
  url(r'test/',test,name="test"),
  url(r'table/',table,name="table"),
  #url(r'vacation/',form_vacation,name="form_vacation"),
  url(r'register/',register,name="register"),
  #url(r'register_save/',save_register,name="save_register"),
  url(r'user_login/',user_login,name="user_login"),
  url(r'user_logout/',user_logout,name="user_logout"), 
  url(r'page/',vacation_page,name="vacation_page"),
  url(r'vacation2/',vacation_form,name="vacation_form"),
  url(r'vacation_save/',save_vacation,name="save_vacation"), 
  url(r'vacation_grid/',vacation_grid,name="vacation_grid"),
  url(r'profile/',profile_form,name="profile_form"),
  url(r'save_profile_user/',save_profile,name="save_profile"),

    ]
