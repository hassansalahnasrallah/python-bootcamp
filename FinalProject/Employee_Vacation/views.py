from django.shortcuts import render,redirect
from . import forms
from Employee_Vacation.forms import UserForm,EmployeeProfileForm,EmployeeVacationForm
from Employee_Vacation.models import Vacation, EmployeeProfile 
# Create your views here.
from django.http.response import HttpResponse
from django.conf.urls import url
from django.contrib.auth.models import User
from dateutil.parser import *
# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import datetime,date
from django.urls import path
from FinalProject import settings
import json
from django.views.decorators.csrf import csrf_protect
import logging
import os
import random
from django.db.models import Q


log = logging.getLogger(__name__)

# Create your views here.
@login_required
def index(request):
      context={}
      user=request.user
      Vacations=Vacation.objects.filter(Employee=user)
      
      context['Vacations']=Vacations
      return render(request, 'index.html', context)
  
@login_required 
def listvacations(request):
    
    """
    Dispaly grid of vacations
    """
    user=request.user
    data=[]
    table_length = request.POST.get('length')
    global_search = request.POST.get('search[value]')
    sorting_column_index = request.POST.get('order[0][column]')
    sorting_column_direction=request.POST.get('order[0][dir]')
    
    sorted_column=request.POST.get('columns[%s][name]' % (sorting_column_index))
    
    qset= Q(Employee=user)
    
    if global_search:
        qset &= Q(Description__icontains=global_search)
        
    Description_search= request.POST.get('columns[0][search][value]')
    if Description_search:
        qset&= Q(Description__icontains=Description_search)
        
    DateFrom_search= request.POST.get('columns[1][search][value]')
    if DateFrom_search:
        qset&= Q(DateFrom__icontains=DateFrom_search)
        
    DateTo_search= request.POST.get('columns[2][search][value]')
    if DateTo_search:
        qset&= Q(DateTo__icontains=DateTo_search)
    
    all_vacations = Vacation.objects.filter(qset).all().order_by("%s%s" % ("-" if sorting_column_direction == "desc" else "",sorted_column))[:int(table_length)]
    
    for vacation in all_vacations:
        vacation.DateFrom=datetime.strftime(vacation.DateFrom, "%B %d, %Y")
        vacation.DateTo=datetime.strftime(vacation.DateTo, "%B %d, %Y")
        data.append({'id': vacation.id,'Description': vacation.Description, 'DateFrom' : vacation.DateFrom , 'DateTo' : vacation.DateTo,'Status' : vacation.Status})
        
    records=len(all_vacations)
    
    response={
        
        'recordsTotal': records,
        'recordsFiltered': records,
        'data': data,
        
         }
    
    return HttpResponse(json.dumps(response))



  
@login_required
def Profile(request):
      context={}
      user=request.user
      EmpProfile=EmployeeProfile.objects.filter(Employee=user)
      
      context['EmpProfile']=EmpProfile
      return render(request, 'Profile.html', context)


@login_required
def special(request):
    # Remember to also set login url in settings.py!
    # LOGIN_URL = '/basic_app/user_login/'
    return HttpResponse("You are logged in. Nice!")

@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered = False

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        profile_form = EmployeeProfileForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.Employee = user

            # Check if they provided a profile picture
            if 'picture' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.picture = request.FILES['picture']

            # Now save model
            profile.save()
            log.debug("Saved profile and user for user: %s", user)
            # Registration Successful!
            registered = True
            return HttpResponseRedirect(reverse('index'))

        else:
            # One of the forms was invalid if this else gets called.
            #print(user_form.errors,profile_form.errors)
            log.debug(user_form.errors,profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = EmployeeProfileForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

def user_login(request):
    loggedin=False
    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                loggedin=True
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('index'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            log.debug("Someone tried to login and failed.")
            log.debug("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'login.html', {})






    
def Retrieve(request,email):
        employees=User.objects.all(email=Email)
        vacation=Vacation.objects.all(employee=employee)
        
        return render(request,"show.html",{'vacation':vacation})
    
def Vacation_page(request):
    context = {}
    
    context['vacations'] = Vacation.objects.all()
    
    return render(request, "vacation_page.html", context)

def vacation_form(request):
    context = {}
    
    Vacation_id = request.GET.get('id')
    vacation = None
    if Vacation_id:
        vacation = Vacation.objects.filter(id=Vacation_id).first()
    
    context['vacation'] = vacation
     
    return render(request, "vacation_form.html", context)

def save_vacation(request):
    print("here")
    Description = request.POST.get('Description')
    Employee = request.user
    Vacation_id = request.POST.get('vacation_id')
    DateFrom = request.POST.get('DateFrom')
    DateTo = request.POST.get('DateTo')
   
    if Description and Employee and DateFrom and DateTo :
        
        if Vacation_id:
            #update
            vacation = Vacation.objects.filter(id=Vacation_id).first()
            
            if vacation:
                vacation.Description = Description
                vacation.Employee = Employee
                DateFrom=datetime.strptime(DateFrom, "%B %d, %Y")
                
                vacation.DateFrom =  DateFrom
                DateTo=datetime.strptime(DateTo, "%B %d, %Y")
                vacation.DateTo = DateTo
                vacation.save()
                
                response = "SUCCESS"
                
            else:
                response = "FAIL"
        else:
            #create
            
            DateFrom=datetime.strptime(DateFrom, "%B %d, %Y")
            DateTo=datetime.strptime(DateTo, "%B %d, %Y")
            Vacation.objects.create(Employee=request.user,Description=Description,DateFrom=DateFrom,DateTo=DateTo)
            response = "SUCCESS"
    else:
        response = "FAIL"
        
    return HttpResponse(response)

""" 

def save_vacation(request):
    print("here")
    Description = request.POST.get('Description')
    Employee = request.user
    Vacation_id = request.POST.get('vacation_id')
    DateFrom = request.POST.get('DateFrom')
    DateTo = request.POST.get('DateTo')
    
    
    status = "OK"
    message = "SUCCESS"
    payload = {}
   
    try:
   
        if Description and Employee and DateFrom and DateTo :
        
            if Vacation_id:
            #update
                vacation = Vacation.objects.filter(id=Vacation_id).first()
                print(vacation)
                if vacation:
                    vacation.Description = Description
                    vacation.Employee = Employee
                    DateFrom=datetime.strptime(DateFrom, "%B %d, %Y")
                
                    vacation.DateFrom =  DateFrom
                    DateTo=datetime.strptime(DateTo, "%B %d, %Y")
                    vacation.DateTo = DateTo
                    vacation.save()
                    payload['id'] = vacation.id
                else:
                    message = "VACATION_NOT_FOUND"
                    status = "FAIL"
            else:
            #create
                print('create')
                DateFrom=datetime.strptime(DateFrom, "%B %d, %Y")
                DateTo=datetime.strptime(DateTo, "%B %d, %Y")
                Vacation.objects.create(Employee=request.user,Description=Description,DateFrom=DateFrom,DateTo=DateTo)
                payload['id'] = vacation.id
        else:
            message = "MISSING_REQUIRED_PARAMETERS"
            status = "FAIL"
    except IntegrityError:
        status = "FAIL"yes the backend part
        message = "VACATION_ALREADY_EXISTS"   
        
    except:
        status = "FAIL"
        message = "SYSTEM_ERROR" 
        log.error("Error while saving VACATION", exc_info=1)
        
    response = {"status": status, "message": message, "payload": payload}
    
    return HttpResponse(json.dumps(response))   
 """       
  

def Add_Vacation(request):  
    print('new vacation')
    if request.method == "POST": 
         
        vacationform = EmployeeVacationForm(data=request.POST)  
       
        if vacationform.is_valid():  
           
            vacation = vacationform.save(commit=False)
            vacation.Employee=request.user  
            vacation.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            print(vacationform.errors)
    else:  
        vacationform = EmployeeVacationForm()   
    return render(request,'vacation.html',{'vacationform':vacationform})  

@login_required
def Profile_form(request):
    context = {}
    
    user = request.user
    
    profile = EmployeeProfile.objects.filter(Employee=user).first()
    
    context['profile'] = profile
    context['MEDIA_URL'] = settings.MEDIA_URL
    return render(request, "profile_form.html", context)


def save_profile(request):
    status = "OK"
    message = "SUCCESS"
    payload = {}
    
    profile_img = request.FILES['profile_img']
    JobPosition = request.POST.get('JobPosition')
    DateOfBirth = request.POST.get('DateOfBirth')
    #DateOfBirth = datetime.strptime(DateOfBirth, "%B %d, %Y")
    
    try:
        log.debug("Profile image: %s", profile_img)  
        
        #define media prefix
        mediaPrefix = ("%s/%s") % (date.today().year, date.today().month)
        #define mediapath directory
        mediaPathDirectory = ("%s/%s") % (settings.MEDIA_ROOT, mediaPrefix)
        
        #check if path exists
        if not os.path.exists(mediaPathDirectory):
            # create media path dir if not found
            os.makedirs(mediaPathDirectory)
        
        #check image extension
        extension = profile_img.name.split(u'.')[-1]  
        
        #rename profile image
        new_filename = "profile-pic-%s.%s" % (random.randint(0, 10000), extension)
        
        #set path
        path = os.path.join(mediaPathDirectory, new_filename)
        dest = open(path, 'wb+')
        
        #write image into dest
        #chunk means to read file peace by peace
        for chunk in profile_img.chunks():
            dest.write(chunk)
            dest.close()
            
        image_url = "%s/%s" % (mediaPrefix, new_filename)
        
        user_profile = EmployeeProfile.objects.filter(Employee_id=request.user.id).first()
        if not user_profile:
            user_profile = EmployeeProfile.objects.create(Employee_id=request.user.id)
            log.debug("user profile not found, creating a new one")
        
        user_profile.picture = image_url
        user_profile.JobPosition = JobPosition
        user_profile.DateOfBirth = DateOfBirth
        user_profile.save()
        log.debug("Saved profile image successfully for user: %s", request.user.id)
        
    except:
        status = "FAIL"
        message = "SYSTEM_ERROR" 
        log.error("Error while saving profile", exc_info=1)
    
    response = {"status": status, "message": message, "payload": payload}
    
    return HttpResponse(json.dumps(response))

@login_required   
def updateProfile(request):  
    context={}
    user=request.user
    EmpProfile=EmployeeProfile.objects.filter(Employee=user) 
    context['EmpProfile']=EmpProfile
    ProfileForm= EmployeeProfileForm(request.POST, instance = EmpProfile)  
    if ProfileForm.is_valid():  
        form.save()  
       # return redirect("/Profile")  
    return render(request, 'edit.html', context)  


def updatestatus(request):
    Vacation_id = request.POST.get('vacation_id')
    
    vacation = Vacation.objects.filter(id=Vacation_id).first()
    if vacation.Status == 'True':
        vacation.Status = 'False'
    else:
        vacation.Status='True'
        
        
    
    
    
urlpatterns=[
    
    url(r"register/",register,name='register'),
    url(r"user_login/",user_login,name='user_login'),
    url(r"logout/",user_logout,name='logout'),
    url(r"edit/",updateProfile,name='edit'),
    url(r"vacationform/", vacation_form, name="vacation_form"),
    url(r"vacation_save/", save_vacation, name="save_vacation"),
    url(r"page/", Vacation_page, name="Vacation_page"),
    path('NewVacation/', Add_Vacation),
    url(r"ShowProfile/",Profile_form,name='Profile_form'),
    url(r"updateProfile/",updateProfile,name='updateProfile'),
    url(r"listvacations/",listvacations,name='listvacations'),
    url(r"updateprofile/",save_profile,name='save_profile'),
    
    ]