from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect, response
from django.conf.urls import url
from Vacations.models import *
from Project import forms
from django.contrib.auth import authenticate, login, logout
from django.urls.base import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.


def home(request):
    return HttpResponse("<h1>This is the Home Page.</h1>")


def index(request):

    context = {'emp': EmployeeProfile.objects.all()}

    return render(request, "Vacations/index.html", context)


@login_required
def form_VacationForm(request):
    form = forms.VacationInfoForm()

    if request.method == 'POST':
        form = forms.VacationInfoForm(data=request.POST)

        if form.is_valid():
            form.save(commit=False)
            # user_id=request.session['_auth_user_id']
            #forms.Vacation.emp_name = User.objects.get()
            user = request.user
            Vacation.user = user
            form.save()

            return index(request)

        else:
            print("Error Saving.")

    context = {'form': form}
    return render(request, 'Vacations/web_page.html', context)


def register(request):

    user_form = forms.UserForm
    profile_form = forms.UserProfileInfoForm

    registered = False

    if request.method == 'POST':
        user_form = forms.UserForm(data=request.POST)
        profile_form = forms.UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # save user to DB:
            user = user_form.save()
            # encrypt password:
            user.set_password(user.password)
            # update user:
            user.save()
            # can't commit => still need to edit profile
            profile = profile_form.save(commit=False)

            # check if profile pic provided
            if 'profile_pic' in request.FILES:
                print("picture found")
                profile.profile_pic = request.FILES['profile_pic']

            profile.user = user
            profile.save()
            registered = True

        else:
            print("not valid.")

    else:
        print("not valid request.")

    context = {'user_form': user_form,
               'profile_form': profile_form, 'registered': registered}
    return render(request, 'Vacations/registration.html', context)


def user_login(request):

    context = {}

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        # django built in authentication function
        user = authenticate(username=username, password=password)
        # get user obj by username
        # if valid -> check if active -> if true ->login

        if user:
            if user.is_active:
                # session
                login(request, user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("Your account is not active.")
        else:
            return HttpResponse("Invalid Login Details.")

    else:

        return render(request, 'Vacations/login.html', context)

    return render(request, 'Vacations/login.html', context)


def vacation_list(request):
    order_by = request.GET.get('order_by', 'defaultOrderField')
    context = {'Desc': Vacation.objects.order_by(
        'desc'), 'Desc2': Vacation.objects.all()}

    return render(request, 'Vacations/list_vacations.html', context)


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return render(request, 'Vacations/login.html')


urlpatterns = [
    url(r'index/', index, name='index'),
    url(r'webpage/', form_VacationForm, name='form_VacationForm'),
    url(r'register/', register, name='register'),
    url(r'user_login/', user_login, name='user_login'),
    url(r'vacations/', vacation_list, name='vacation_list'),
    url(r'logout/', logout_request, name='logout_request'),

]
