from django.shortcuts import render
from django.template.context_processors import request
from django.http.response import HttpResponse
from django.conf.urls.i18n import urlpatterns
from django.conf.urls import url
# Create your views here.

def index(request):
    return HttpResponse("Hello Im Jarvis ")

def index2(request):
    return HttpResponse("Glad to Meet you Sir ")

def index3(request):
    return HttpResponse("what is your name ")



urlpatterns= [
    url(r"index/",index,name= "index"),
    url(r"index_2/",index2,name= "index2"),
    url(r"index_3/",index3,name= "index3"),
    
    
    
    ]