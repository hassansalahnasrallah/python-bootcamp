from django.shortcuts import render
from lib2to3.fixes.fix_input import context
from web_app import forms
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls.base import reverse
from web_app import models, forms
from django.contrib.auth.models import AbstractUser
from .models import User
from django.contrib.auth.decorators import login_required
from django.template.context_processors import request
from web_project import settings

def register(request):
    
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
            if 'picture' in request.FILES:
                print("found the picture")
                profile.picture = request.FILES['picture']
            profile.user = user
            profile.save()
            
    context = {'user_form': forms.UserForm, 'profile_form':forms.UserProfileInfoForm }
    return render(request, 'registration.html', context)


#urlpatterns = [
 #   url("register", register, name="register"),]

def login_1(request):
    context={}
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        
    
        user =authenticate(username=username, password=password)
   
        if user:
            
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        
        else:
            
           
            return  render(request, 'login.html' ,  context)
          
    else:
        return  render(request, "login.html" ,  context)
        HttpResponse("no such user please register a new user")
         
         
    return  render(request, "login.html" ,  context)         
         
         
def profile(request):
    profile_form = forms.UserProfileInfoForm
    if request.method == "POST":
        date=request.POST.get('date')
        print('date')
       
        profile_form = forms.UserProfileInfoForm(data= request.POST)
    
        if profile_form.is_valid():
            current_user = request.user.id
            
            user = models.Userprofile.objects.get(user_id = current_user)
            user.job_description = profile_form.cleaned_data['job_description']
            user.picture = profile_form.cleaned_data['picture']
            user.date = date
            user.save()
            return HttpResponseRedirect(reverse('showvacation'))
        else:
            return HttpResponse('not valid entry')
    context = {'profile_form': forms.UserProfileInfoForm }
    return render(request, 'profile.html', context)




@login_required
def index(request):
    current_user = request.user.id
    print('enterd')
    form = models.Userprofile.objects.filter(user_id = current_user)
    print(form)
    context = {'form':form}
    context['MEDIA_URL'] = settings.MEDIA_URL
    return render(request, 'index.html', context)



def showvacation(request):
    current_user = request.user.id
    print('enterd')
    form = models.Vacation.objects.filter(user_id = current_user)
    print(form)
    context = {'form':form}
    return render(request, 'showvacation.html', context)
    
    
    
    



def vacation(request):
    vacation = forms.vacation
    vacation_id= request.GET.get('id')
    if request.method == "POST":
        datefrom = request.POST.get('datefrom')
        dateto = request.POST.get('dateto')
        vacation = forms.vacation(data= request.POST)
    
        if vacation.is_valid():
            #current_user = request.user.id
            #print(current_user)
            #user = models.Vacation.objects.filter(user_id = current_user)
            #user= request.user.username
           # user.description = vacation.cleaned_data['description']
            #user.datefrom = vacation.cleaned_data['datefrom']
            #user.dateto = vacation.cleaned_data['dateto']
            #for object in user:
                #object.save()
            #current_user = request.user.username
           # print(current_user)
           # user= models.Vacation.objects.filter(user= current_user)
            if vacation_id:
                vacation_save = models.Vacation.objects.get(id = vacation_id)
                vacation_save.description = vacation.cleaned_data['description']
                vacation_save.datefrom = datefrom
                vacation_save.dateto = dateto
                vacation_save.save()
                return HttpResponseRedirect(reverse('showvacation'))
               

            vacation_save= vacation.save(commit=False)
            vacation_save.user_id=request.user.id
            vacation_save.description = vacation.cleaned_data['description']
            vacation_save.datefrom = datefrom
            vacation_save.dateto = dateto
            vacation_save.save()
            return HttpResponseRedirect(reverse('showvacation'))
        else:
            return HttpResponse('not valid entry')
    context = {'vacation': forms.vacation }
    return render(request, 'vacation.html', context)



def jquery(request):
    context= {}
    return render(request, 'jqueryui.html', context)



