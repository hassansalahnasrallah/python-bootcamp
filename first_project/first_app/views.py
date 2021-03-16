from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.conf.urls import url

from . import forms
import profile
from django.contrib.auth import authenticate, login
from django.urls.base import reverse
from django.contrib.auth.decorators import login_required
from first_app.models import Topic
import json
from django.db.utils import IntegrityError

import logging

log = logging.getLogger(__name__)
# Create your views here.

def index(request):
    context = {"help_text": "This is a help text"}
    log.debug("Index")
    log.info("Index ")
    log.warning("warning")
    log.error("ll")
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
            log.debug("Saved profile and user for user: %s", user)
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

def topic_page(request):
    context = {}
    
    context['topics'] = Topic.objects.all()
    
    return render(request, "topic_page.html", context)

def topic_form(request):
    context = {}
    
    log.debug("Now we are in the topic form")
    topic_id = request.GET.get('id')
    topic = None
    if topic_id:
        topic = Topic.objects.filter(id=topic_id).first()
    
    context['topic'] = topic
       
    return render(request, "topic_form.html", context)


def save_topic(request):
    
    topic_name = request.POST.get('topic_name')
    topic_id = request.POST.get('topic_id')
    
    status = "OK"
    message = "SUCCESS"
    payload = {}
    
    try:
        if topic_name:
            
            if topic_id:
                #update
                topic = Topic.objects.filter(id=topic_id).first()
                
                if topic:
                    topic.topic_name = topic_name
                    topic.save()
                    payload['id'] = topic.id
                else:
                    message = "TOPIC_NOT_FOUND"
                    status = "FAIL"
            else:
                #create
                topic = Topic.objects.create(topic_name=topic_name)
                payload['id'] = topic.id
        else:
            message = "MISSING_REQUIRED_PARAMETERS"
            status = "FAIL"
            
    except IntegrityError:
        status = "FAIL"
        message = "TOPIC_NAME_ALREADY_EXISTS"
        
    except:
       status = "FAIL"
       message = "SYSTEM_ERROR" 
       log.error("Error while saving topic name", exc_info=1)
        
    response = {"status": status, "message": message, "payload": payload}
    
    return HttpResponse(json.dumps(response))


def topic_grid(request):
    
    #response = [{'title': "vacation title"}, ]
    
    data = []
    all_topics = Topic.objects.all()
    for topic in all_topics:
        data.append({'topic_name': topic.topic_name})
    
    records = len(all_topics)
    
    response = {
        #'draw': request.GET.get("_"),
        'recordsTotal': records,
        'recordsFiltered': records,
        'data': data,
    }
    
    return HttpResponse(json.dumps(response))

urlpatterns = [
    url(r"topic_grid", topic_grid, name="topic_grid"),
    url(r"index/", index, name="index"),
    url(r"index_2/", index2, name="index2"),
    url(r"index_3/", index3, name="index3"),
    url(r"form/", form_name_view, name="form_name_view"),
    url(r"webpage/", form_webpage, name="form_webpage"),
    url(r"register/", register, name="register"),
    url(r"user_login/", user_login, name="user_login"),
    url(r"topic/", topic_form, name="topic_form"),
    url(r"topic_save/", save_topic, name="save_topic"),
    url(r"page/", topic_page, name="topic_page"),
]