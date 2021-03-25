from django.shortcuts import render

from lib2to3.fixes.fix_input import context

from final_app import forms

from django.contrib.auth import authenticate, login, logout

from django.http.response import HttpResponse, HttpResponseRedirect

from django.urls.base import reverse

from final_app import models

from django.contrib.auth.models import AbstractUser

from .models import User

from django.contrib.auth.decorators import login_required

from django.template.context_processors import request

from django.conf.urls import url

from final_app.forms import UserForm,UserProfileInfoForm

from final_project import settings

def register(request):
    
    registered = False
    user_form = forms.UserForm
    profile_form = forms.UserProfileInfoForm
    if request.method == "POST":
        user_form = forms.UserForm(data= request.POST)
        profile_form = forms.UserProfileInfoForm(data= request.POST)
    
        if user_form.is_valid() and profile_form.is_valid():
            
            user= user_form.save()
            
            user.set_password(user.password)
            
            user.save()
            
            profile = profile_form.save(commit=False)
            
            
            
            if 'profile_pic' in request.FILES:
                
                print("found the picture")
                
                profile.profile_pic = request.FILES['profile_pic']
            profile.user=user
            
            profile.save()
            
            registered = True
         
        else:
                # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)

    else:
            # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'registration.html',
                          {'user_form':forms.UserForm,
                           'profile_form':forms.UserProfileInfoForm,
                           'registered':registered})   
            
    



def login(request):
    
    if request.method == 'POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password')

        
        user = authenticate(username=username, password=password)

        
        if user:
            
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        
        else:
            
           
            return  render(request, 'login.html' ,  {})
          
    else:
        return  render(request, "login.html" ,   {})
        HttpResponse("there is no such user. Please register a new user")
         
         
    return  render(request, "login.html" ,   {})  
         

def profile(request):
    profile_form = forms.UserProfileInfoForm
    if request.method == "POST":
        date = request.POST.get('Date_Of_Birth')
        print('Date_Of_Birth')
        profile_form = forms.UserProfileInfoForm(data = request.POST)
    
        if profile_form.is_valid():
            current_user = request.user.id
            
            user = models.UserProfileInfo.objects.get(user_id = current_user)
            
            user.job_position = profile_form.cleaned_data['job_position']
            
            
            user.profile_pic = profile_form.cleaned_data['profile_pic']
            
            user.date = date
            
            user.save()
            return HttpResponseRedirect(reverse('vacation_forms'))
        else:
            return HttpResponse('there is no valid entry')
    context = {'profile_form': forms.UserProfileInfoForm }
    return render(request, 'profile.html', context)




@login_required(login_url='login')
def index(request):
    current_user = request.user.id
    print('entered')
    form = models.UserProfileInfo.objects.filter(user_id = current_user)
    print(form)
    context = {'form':form}
    context['MEDIA_URL'] = settings.MEDIA_URL
    return render(request, 'index.html', context)


@login_required(login_url='login')
def vacation_forms(request):
    current_user = request.user.id
    print('you have entered')
    form = models.Vacation.objects.filter(user_id = current_user)
    print(form)
    context = {'form':form}
    return render(request, 'vacation_forms.html', context)
  
def vacation(request):
    vacation = forms.vacation
    vacation_id= request.GET.get('id')
    if request.method == "POST":
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        vacation = forms.vacation(data= request.POST)
    
        if vacation.is_valid():
        
            if vacation_id:
                vacation_save = models.Vacation.objects.get(id = vacation_id)
                vacation_save.description = vacation.cleaned_data['description']
                vacation_save.date_from = date_from
                vacation_save.date_to = date_to
                vacation_save.save()
                return HttpResponseRedirect(reverse('vacation_forms'))
               

            vacation_save= vacation.save(commit=False)
            vacation_save.user_id=request.user.id
            vacation_save.description = vacation.cleaned_data['description']
            vacation_save.date_from = date_from
            vacation_save.date_to = date_to
            vacation_save.save()
            return HttpResponseRedirect(reverse('vacation_forms'))
        else:
            return HttpResponse('no valid entry')
    context = {'vacation': forms.vacation }
    return render(request, 'vacation.html', context)




def user_logout(request):
    logout(request)

    return HttpResponseRedirect(reverse('login'))

def test(request):
    context={}
    return render(request,'test.html',context)
urlpatterns = [
    
    url(r'register',register , name='register'),
    url(r'login', login , name='login'),
    url(r'profile',profile, name='profile'),
    url(r'index', index, name='index'),
    url(r'vacation',vacation, name='vacation'),
    url(r'vacation_forms',vacation_forms, name='vacation_forms'),
    url(r'logout', user_logout, name='logout'),
    url(r'test', test, name='test')
    ]