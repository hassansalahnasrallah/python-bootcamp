from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, response
from django.conf.urls import url
from Vacations.models import *
from Project import forms
from django.contrib.auth import authenticate, login, logout
from django.urls.base import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from Project import settings

#to get console debug/log 
import logging
import json
from django.db.models import Q
from Project.forms import VacationInfoForm
log = logging.getLogger(__name__)


# Create your views here.
def home(request):
    return HttpResponse("<h1>This is the Home Page.</h1>")

@login_required
def index(request):
    """
    Main page to view user profile 
    """

    context = {}

    context['MEDIA_URL'] = settings.MEDIA_URL
    context['emp'] = EmployeeProfile.objects.filter(user_id=request.user.id).first()
    #context['emp'] = EmployeeProfile.objects.all()
    #context ['emp'] : emp

    return render(request, "Vacations/index.html", context)


@login_required
#def form_vacation
def form_VacationForm(request):
    """
    On form validated, create vacation and assign it to the logged in user
    On success, redirect to the vacation list
    """
    form = forms.VacationInfoForm()
    
    if request.method == 'POST':
        form = forms.VacationInfoForm(data=request.POST)

        if form.is_valid():
            vacation = form.save(commit=False)
            vacation.user = request.user
            vacation.save()
            log.debug("Vacation successfully added for user: %s",vacation.user)
            return vacation_list(request)


        else:
           # print("Error Saving.")
            log.error("failed to save...")

    context = {'form': form}
    return render(request, 'Vacations/vacation_form.html', context)


def register(request):
    """
    user inserts required data to DB
    """
    status = "OK"
    message = "SUCCESS"
    payload = {}

    user_form = forms.UserForm
    profile_form = forms.UserProfileInfoForm

    registered = False
    try:
        if request.method == 'POST':
            user_form = forms.UserForm(data=request.POST)
            profile_form = forms.UserProfileInfoForm(data=request.POST)

            if user_form.is_valid() and profile_form.is_valid():
                # save user to DB:
                user = user_form.save()
                # encrypt password:
                user.set_password(user.password)
                # update user:
                user.save()
                # can't commit => still need to edit profile
                profile = profile_form.save(commit=False)

                # check if profile pic provided
                if 'profile_pic' in request.FILES:
                    print("picture found")
                    profile.profile_pic = request.FILES['profile_pic']

                profile.user = user
                profile.save()
                log.debug("Profile saved successfully for user: %s", User)
                registered = True
                return render(request, 'Vacations/login.html')
                return render('vacations.login.html', message='Save complete')

            # else:
            #     log.error("Error while creating user ", exc_info=1)

    except:
        status = "FAIL"
        message = "SYSTEM_ERROR" 
        log.debug("Error while creating user", exc_info=1)

    response = {"status": status, "message": message, "payload": payload}

    #return HttpResponse(json.dumps(response))

    context = {'user_form': user_form,
               'profile_form': profile_form, 'registered': registered}
    return render(request, 'Vacations/registration.html', context)


def user_login(request):
    """
    user login through username & password to manage vacations
    """

    context = {}

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        # django built in authentication function
        user = authenticate(username=username, password=password)
        # get user obj by username
        # if valid -> check if active -> if true ->login

        if user:
            if user.is_active:
                # session
                login(request, user)
                log.debug("user logged in: %s", User)
                return HttpResponseRedirect(reverse('index'))

            else:
                log.error(" account is not active for user: %s", user)
                return HttpResponse("Your account is not active.")

        else:
            log.error("Invalid Login Details for user: %s", user)
            return HttpResponse("Invalid Login Details.")

    else:
      
        return render(request, 'Vacations/login.html', context)
  
    return render(request, 'Vacations/login.html', context)


@login_required
def vacation_list(request):
    """
    get list of vacation filter by logged in user
    """
    context = {}
    
    vacation_list = Vacation.objects.filter(user=request.user).all()

    context['vacations'] = vacation_list

    return render(request, 'Vacations/list_vacations.html', context)


def logout_request(request):
    """
    login out for user page
    """

    logout(request)
    log.debug("user logged out%s",request.user.id)
    return render(request, 'Vacations/login.html')


def validate_username(request):
    """
    Check username availability
    """
    username = request.GET.get('username', None)
    email = request.GET.get('email', None)
    
    # email = User.object.get(email=request.user.email)
    response = {
        'is_taken': User.objects.filter(username__iexact=username).exists(),
        #'is_taken2': User.objects.filter(email__iexact=email).exists(), to validate unique email 

    }
    return JsonResponse(response)



@login_required
def edit_profile(request):
    """
    user updates his existing profile
    """
    form = VacationInfoForm()
    if request.method == 'POST':
        user_form = forms.UserForm(data = request.POST,instance = request.user)

        profile_form =forms.UserProfileInfoForm(data=request.POST,instance=request.user.employeeprofile)

        if user_form.is_valid() and profile_form.is_valid():
                # save user to DB:
                user = user_form.save()
                # encrypt password:
                user.set_password(user.password)
                # update user:
                user.save()
                # can't commit => still need to edit profile
                profile = profile_form.save(commit=False)

                # check if profile pic provided
                if 'profile_pic' in request.FILES:
                    print("picture found")
                    profile.profile_pic = request.FILES['profile_pic']

                profile.user = user
                profile.save()
                log.debug("Profile saved successfully for user: %s", user)

                return render(request, 'Vacations/edit_profile.html')

    else:
        user_form = forms.UserForm(instance = request.user)
        profile_form = forms.UserProfileInfoForm(instance = request.user)

    context = {
            'user_form':user_form,
            'profile_form':profile_form
     }
    return render(request,'Vacations/edit_profile.html',context)

@login_required
def edit_vacation(request):
 
    context = {}
    desc = request.POST.get('desc')
    from_date = request.POST.get('from_date')
    to_date = request.POST.get('to_date')
   
    vacation_id = request.POST.get('vacation_id')
    #vacation = vacation.objects.filter(id=vacation_id).first()

    
    try:
        vacation = Vacation.objects.filter(id=vacation_id).first()

      
            
            # if vacation_id:
        if vacation_id:

                #update
                vacation_des = Vacation.desc
                vacation_from_date = Vacation.from_date
                vacation_to_date = Vacation.to_date
                

                #vacation = vacation.objects.filter(id=vacation_id).first()
                vacation.save()
                log.debug("vacation updated successfully")
        else:
                vacation = Vacation(user_id=request.user.id)
   
                
       
                log.error("failed to update")


    except Exception:
        log.error("Error while saving vacation", exc_info=1)
    form = forms.VacationInfoForm()
   # vacation_form = forms.VacationInfoForm(data=request.POST,instance=request.user.id)

    vacation_id = request.POST.get('vacation_id')       
    context = {'vacation' : Vacation.objects.filter(id=vacation_id).first(),
    'forms': VacationInfoForm}
    
    return render(request,'Vacations/edit_vacation.html',context)





 
urlpatterns = [
    url(r'index/', index, name='index'),
    url(r'vacationform/', form_VacationForm, name='form_VacationForm'),
    url(r'register/', register, name='register'),
    url(r'user_login/', user_login, name='user_login'),
    url(r'vacations/', vacation_list, name='vacation_list'),
    url(r'logout/', logout_request, name='logout_request'),
    url(r'validate_username', validate_username, name='validate_username'),
   
    url(r'edit_profile/', edit_profile, name='edit_profile'),
    url(r'edit_vacation/', edit_vacation, name='edit_vacation'),


    

]