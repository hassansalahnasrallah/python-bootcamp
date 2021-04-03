"""web_project URL Configuration

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
from web_app import views
from web_project import settings
from django.conf.urls import url
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register', views.register , name='register'),
    path('login', views.login_1 , name='login'),
    path('profile', views.profile, name='profile'),
    path('index', views.index, name='index'),
    path('vacation', views.vacation, name='vacation'),
    path('showvacation',views.showvacation, name='showvacation'),
    path('jqueryui',views.jquery, name='jquery'),
    url(r'^logout', views.userlogout, name='logout'),
    url(r'^', views.home, name='home'),
    ] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
