"""finalproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from finalapp import views
from django.conf.urls import url,include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    url(r'^User_Login/',include('finalapp.urls')),
    url('admin/', admin.site.urls),
    url(r'^$',views.index,name='index'),
    url(r'^SignUp/',views.SignUp,name='SignUp'),
    url(r'^save_vacation/',views.save_vacation,name='save_vacation'),
    url(r'^VacationForm/',views.VacationForm,name='VacationForm'),
    url(r'^Home/',views.Home,name='Home'),
    url(r'^Profile/',views.Profile,name='Profile'),
    url(r'^Logout/',views.Logout,name='Logout'),
    url(r'^jquery/',views.jquery,name='jquery'),
   
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
