from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.conf.urls import url
from . import forms
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from final_app.models import Vacation

# Create your views here.

def index(request):
    context={}
    return render(request, 'index.html', context)

def test(request):
    context={}
    return render(request, 'test.html', context)

@login_required
def table(request):
    context={}
    return render(request, 'table.html', context)

#@login_required
#def form_vacation(request):
#     form=forms.VacationForm()
#    
#    
#     if request.method == 'POST':
#           form=forms.VacationForm(request.POST)
#           
#           if form.is_valid():
#                form.save(commit=True)
#                return index(request)
#           else:
#                print("ERROR")
          
          
                    
                
#     context={'form':form} 
         
#     return render(request,'vacation.html',context) 

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

def vacation_page(request):
    
    context = {}
    
    context['vacations'] = Vacation.objects.all()
    
    return render (request,'vacation_page.html',context)

def vacation_form(request):
    
    context = {}
    
    description_id = request.GET.get('id')
    desc=None
    if description_id:
        desc = Vacation.objects.filter(id=description_id).first()
        print("there is a vacation id")
        
    
    context['desc'] = desc
    
    return render(request,'vacation_form.html',context)

def save_vacation(request):     
    
    description = request.POST.get('description')
    description_id = request.POST.get('description_id')
    #desc
    
    if description: #and and and 
        
        if description_id:
            #update
            desc = Vacation.objects.filter(id = description_id).first()
            
            if desc:
                desc.description = description
                desc.save()
                response = "SUCCESS"
            else:
                 response = "FAIL"
                
        else:
            #create
            Vacation.objects.create(description=description )
            response = "SUCCESS"
            
    else:
        response = "FAIL!"
    
    return HttpResponse(response)

urlpatterns = [
    
  url(r'index/',index,name="index"),
  url(r'test/',test,name="test"),
  url(r'table/',table,name="table"),
  #url(r'vacation/',form_vacation,name="form_vacation"),
  url(r'register/',register,name="register"),
  url(r'user_login/',user_login,name="user_login"), 
  url(r'page/',vacation_page,name="vacation_page"),
  url(r'vacation2/',vacation_form,name="vacation_form"),
  url(r'vacation_save/',save_vacation,name="save_vacation"),
    ]
