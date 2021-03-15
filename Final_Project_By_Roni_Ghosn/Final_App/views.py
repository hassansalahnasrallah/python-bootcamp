from django.shortcuts import render

from lib2to3.fixes.fix_input import context

from Final_App import forms

from django.contrib.auth import authenticate, login

from django.http.response import HttpResponse, HttpResponseRedirect

from django.urls.base import reverse

from Final_App import models

from django.contrib.auth.models import AbstractUser

from .models import User

from django.contrib.auth.decorators import login_required

from django.template.context_processors import request

from django.conf.urls import url

from Final_App.forms import UserForm, UserProfileInfoForm


def register(request):
    registered = False
    # user_form = forms.UserForm
    # profile_form = forms.UserProfileInfoForm
    if request.method == "POST":
        user_form = forms.UserForm(data=request.POST)
        profile_form = forms.UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()

            user.set_password(user.password)

            user.save()

            profile = profile_form.save(commit=False)

            profile.user = user

            if 'profile_pic' in request.FILES:
                print("found the picture")

                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors, profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request, 'registration.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


def login(request):
    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            # Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request, user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('index'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        # Nothing has been provided for username or password.
        return render(request, 'login.html', {})


@login_required(login_url='login')
def profile(request):
    profile_form = forms.UserProfileInfoForm
    if request.method == "POST":

        profile_form = forms.UserProfileInfoForm(data=request.POST)

        if profile_form.is_valid():
            current_user = request.user.id

            user = models.UserProfileInfo.objects.get(user_id=current_user)

            user.job_position = profile_form.cleaned_data['job_position']

            user.profile_pic = profile_form.cleaned_data['profile_pic']

            user.Date_Of_Birth = profile_form.cleaned_data['Date_Of_Birth']

            user.save()
            return HttpResponseRedirect(reverse('vacation_forms'))
        else:
            return HttpResponse('there is no valid entry')
    context = {'profile_form': forms.UserProfileInfoForm}
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def index(request):
    current_user = request.user.id
    print('entered')
    form = models.UserProfileInfo.objects.filter(user_id=current_user)
    print(form)
    context = {'form': form}
    return render(request, 'index.html', context)


def vacation_forms(request):
    current_user = request.user.id
    print('entered')
    form = models.Vacation.objects.filter(user_id=current_user)
    print(form)
    context = {'form': form}
    return render(request, 'vacation_forms.html', context)


def showformdata(request):
    # form = forms.UserForm
    if request.method == 'POST':
        form = forms.UserForm(data=request.POST)
        if form.is_valid():
            nam = form.cleaned_data['job_position']
            eml = fm.cleaned_data['profile_pic']
            pswrd = fm.cleaned_data['password']
            regstr = User(username='Wissam', name=nam, email=eml, password=pswrd)
            regstr.save()
    else:
        form = register(request)
    return render(request, "profile.html", {'form': form})


def vacation(request):
    vacation = forms.vacation
    vacation_id = request.GET.get('id')
    if request.method == "POST":

        vacation = forms.vacation(data=request.POST)

        if vacation.is_valid():

            if vacation_id:
                vacation_save = models.Vacation.objects.get(id=vacation_id)
                vacation_save.description = vacation.cleaned_data['description']
                vacation_save.date_from = vacation.cleaned_data['date_from']
                vacation_save.date_to = vacation.cleaned_data['date_to']
                vacation_save.save()
                return HttpResponseRedirect(reverse('vacation_forms'))

            vacation_save = vacation.save(commit=False)
            vacation_save.user_id = request.user.id
            vacation_save.save()
            return HttpResponseRedirect(reverse('vacation_forms'))
        else:
            return HttpResponse('not valid entry')
    context = {'vacation': forms.vacation}
    return render(request, 'vacation.html', context)


def test(request):
    context = {}
    return render(request, 'test.html', context)


urlpatterns = [

    url(r'register', register, name='register'),
    url(r'login', login, name='login'),
    url(r'profile', profile, name='profile'),
    url(r'index', index, name='index'),
    url(r'vacation', vacation, name='vacation'),
    url(r'vacation_forms', vacation_forms, name='vacation_forms'),
    url(r'test', test, name='test'),
]