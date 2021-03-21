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
# Create your views here.

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
                return HttpResponseRedirect(reverse('vacation'))
            else:
                return HttpResponse("Not connected")
        else:
            return HttpResponse("User not found")
    else:
         return render(request,'login.html', context)
    
    return render(request,'login.html',context)


def Signup(request):
   # userprofileinfo=forms.UserInfo()
    signup_form=forms.FormSignup()
    sign_up=False
    
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
            return HttpResponseRedirect(reverse('login'))
        else:
             print("User not found")
    else:
        print("Not valid")

    context={'signup_form':signup_form,'sign_up':sign_up}

    return render(request,'signup.html',context)

@login_required
def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

@login_required()
def EditProfile(request):
     context={}
     user_id=request.GET.get('id')
     user_profile=None
     if user_id:
         user_profile=UserProfile.objects.filter(id=user_id).first()
     context['vacation']=vacation
     return render(request,'EditProfile.html',context)


# @login_required()
# def Profile(request):
    # user=request.user
    # profile=UserProfile.objects.get(user_id=user.id)
    # form=forms.UserProfileForm(instance=profile)
    # if request.method=='POST':
        # form = forms.UserProfileForm(data=request.POST,instance=profile)
        # if form.is_valid():
            # form.save()
    # context={'form':form}
    # return render(request,'EditProfile.html',context)

# def save_profile(request):
    # user=request.user
    # job_position=request.POST.get("Jposition")
    # dateofbirth=request.POST.get("date_of_birth")
    # profilepicture=request.POST.get("P-pic")
    # user_id=request.POST.get("user_id")
    # if job_position and dateofbirth and profilepicture:
        # if vacation_id:
            # user_profile=UserProfile.objects.filter(id=user_id).first()
            # if vacation:
                # user_profile.job_position=job_position
                # user_profile.dateofbirth=dateofbirth
                # user_profilepicture=profilepicture
                # user_profile.save()
        # else:
            # UserProfile.objects.create(user=user,job_position=job_position,dateofbirth=dateofbirth,profilepicture=profilepicture)
    # return HttpResponseRedirect(reverse('vacation'))


@login_required()
def vacation(request):
    context={}
    context['vacations']=Vacation.objects.all()
    return render(request,'vacation.html',context)


@login_required()
def AddV(request):
    context={}
    vacation_id=request.GET.get('id')
    vacation=None
    if vacation_id:
        vacation=Vacation.objects.filter(id=vacation_id).first()
    context['vacation']=vacation
    return render(request,'Addv.html',context)


def save(request):
    user=request.user
    description=request.POST.get("desc")
    datefrom=request.POST.get("date_from")
    dateto=request.POST.get("date_to")
    vacation_id=request.POST.get("vacation_id")
    status="OK"
    message="SUCCESS"
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
    except IntegrityError:
        message="VACATION_NAME_DUPLICATE"
        status="FAIL"
    except:
        message="SYSTEM_ERROR"
        status="FAIL"
    response={"status":status,"message":message,"payload":payload}
    return HttpResponseRedirect(reverse('vacation'))

def profile_form(request):
    context = {}
    
    context['MEDIA_URL'] = settings.MEDIA_URL
    context['user_profile'] = UserProfile.objects.filter(user_id=request.user.id).first()
    
    return render(request, "profile_form.html", context)

def save_profile(request):
    status = "OK"
    message = "SUCCESS"
    payload = {}
    
    profile_pic = request.FILES['p_pic']
    dateofbirth=request.POST.get("date_of_birth")
    job_position=request.POST.get("Jposition")
    
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
        
        user_profile = UserProfile.objects.filter(user_id=request.user.id).first()
        if not user_profile:
            user_profile = UserProfile.objects.create(user_id=request.user.id)
            log.debug("user profile not found, creating a new one")
        
        user_profile.picture = image_url
        user_profile.portfolio = portfolio
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
    url(r'logout/',Logout,name='logout'),
    url(r'signup/',Signup,name='sign_up'),
    url(r'EditProfile/',EditProfile,name='EditProfile'),
    url(r'vacation/',vacation,name='vacation'),
    url(r'AddV',AddV,name='AddV'),
    url(r"save/",save,name="save"),
    url(r"save_profile/",save_profile,name="save_profile"),
    ]