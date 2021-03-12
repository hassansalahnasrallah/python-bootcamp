from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.conf.urls import url
from . import forms
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    context={}
    return render(request, 'index.html', context)

@login_required
def table(request):
    context={}
    return render(request, 'table.html', context)

@login_required
def form_vacation(request):
     form=forms.VacationForm()
    
    
     if request.method == 'POST':
           form=forms.VacationForm(request.POST)
           
           if form.is_valid():
                form.save(commit=True)
                return index(request)
           else:
                print("ERROR")
          
          
                    
                
     context={'form':form} 
         
     return render(request,'vacation.html',context) 

def register(request):   
    
    user_form=forms.UserForm
    profile_form=forms.UserProfileInfoForm
    
    registered=False
    
    if request.method == "POST":
        
        user_form = forms.UserForm(data=request.POST)
        profile_form=forms.UserProfileInfoForm(data=request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            
            print("form valid")
            #save data
            user=user_form.save()
            user.set_password(user.password)
            
            user.save()
            
            profile=profile_form.save(commit=False)
            #commit=false prevent to save the profile bbecause still need to edit profile (bdna User)
            
            profile.user=user
            
            #check if profile pic provided
            if 'picture' in request.FILES:
                print("found the picture")
                profile.picture=request.FILES['picture']
            
            
            profile.save()
            
            registered=True
            
        else:
            print("form not valid")
            
    else:
        print("Not valid request")  
              
    context={'user_form':user_form,'profile_form':profile_form,'registered':registered}
    
    return render(request,'registration.html',context)

def user_login(request):
    
    
    context={}
    
    if request.method == 'POST':
        username=request.POST.get('username') 
        password=request.POST.get('password')
        
        
        #django built in authentication
        
        user=authenticate(username=username,password=password)
        #check if username valid then if active
        
        if user:
            
            if user.is_active:
                login(request,user)
                
                return HttpResponseRedirect( reverse('table'))


            
            else:
                return HttpResponse("Your account is not active") 
            
        else:
            return HttpResponse("Invalid login details")
                  
    else:
        return render (request,'login.html',context)
        
    
    return render (request,'login.html',context)          


urlpatterns = [
    
  url(r'index/',index,name="index"),
  url(r'table/',table,name="table"),
  url(r'vacation/',form_vacation,name="form_vacation"),
  url(r'register/',register,name="register"),
  url(r'user_login/',user_login,name="user_login"), 

    ]
