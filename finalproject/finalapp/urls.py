
from django.conf.urls import url
from finalapp import views

app_name = 'finalapp'

urlpatterns = [
    url(r'^$',views.User_Login,name='User_Login'),
]
