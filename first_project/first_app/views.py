from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.conf.urls import url

from . import forms
import profile
from django.contrib.auth import authenticate, login
from django.urls.base import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    context = {"help_text": "This is a help text"}
    return render(request, "first_app/index.html", context)


def index2(request):
    return HttpResponse("hello world 2")


def index3(request):
    return HttpResponse("hello world 3")


def form_name_view(request):
    
    form = forms.FormName()
    
    if request.method == 'POST':
        form = forms.FormName(request.POST)
        
        if form.is_valid():
            print("Validation Success")
    
    context = {'form': form}
    
    return render(request, 'form_page.html', context)
   
   
@login_required
def form_webpage(request):
    
    form = forms.WebPageForm()
    
    if request.method == "POST":
        form = forms.WebPageForm(request.POST)
        
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print("Error")
     
    context = {'form': form}       
    
    return render(request, 'web_page.html', context)
    

def register(request): 
    user_form = forms.UserForm
    profile_form =  forms.UserProfileInfoForm
    
    registered = False
    if request.method == "POST":
        
        user_form = forms.UserForm(data=request.POST)
        profile_form = forms.UserProfileInfoForm(data=request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            
            #save user to database
            user = user_form.save()
            
            #Hash the password
            user.set_password(user.password)
            
            #Update user with hashed password
            user.save()
            
            #can't commit because we still need to edit profile
            profile = profile_form.save(commit=False)
            
            #check if profile pic provided
            if 'picture' in request.FILES:
                print("Found the picture")
                profile.picture = request.FILES['picture']
            
            profile.user = user
            profile.save()
            
            registered = True
        else:
            print("Form not valid")
    
    else:
        print("Not valid request")
    
    context = {"user_form": user_form, 'profile_form': profile_form, 'registered': registered}
       
    return render(request, 'registration.html', context)
    
def user_login(request):
    
    context = {}
    
    if request.method == 'POST':
        username = request.POST.get('username') #request.POST['username']
        password = request.POST.get('password')
        
        #django built in autentication function
        user = authenticate(username=username, password=password)
        #get USer object by username, if valid check password if match if valid, check if user is active then login
        
        #If we have a user
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Your account is not active')
        else:
            return HttpResponse("Invalid login details")
    else:
        return render(request, "login.html", context)
    
    return render(request, "login.html", context)

urlpatterns = [
    
    url(r"index/", index, name="index"),
    url(r"index_2/", index2, name="index2"),
    url(r"index_3/", index3, name="index3"),
    url(r"form/", form_name_view, name="form_name_view"),
    url(r"webpage/", form_webpage, name="form_webpage"),
    url(r"register/", register, name="register"),
    url(r"user_login/", user_login, name="user_login"),
    
]