from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout

from user.forms import RegistrationForm, AccountAuthenticationForm
from .models import User

from django.contrib.auth.decorators import login_required



def home(request):
    return render(request, "home.html")    

def register_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse("You are already authenticated as " + str(user.email))

    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            destination = kwargs.get("next")
            if destination:
                return redirect(destination)
            return redirect('login')
        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'user/register.html', context)


def logout_view(request):
    logout(request)
    return redirect("login")


def login_view(request, *args, **kwargs):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("video")

    destination = get_redirect_if_exists(request)
    print("destination: " + str(destination))

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                if destination:
                    return redirect(destination)
                return redirect("video")

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form

    return render(request, "user/login.html", context)


def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
    return redirect


#@login_required  # Require user logged in before they can access profile page
#def profile_view(request):
#    if request.method == 'POST':
#        u_form = UserUpdateForm(request.POST, instance=request.user)
#        p_form = ProfileUpdateForm(request.POST,
#                                   request.FILES,
#                                   instance=request.user.profile)
#        if u_form.is_valid() and p_form.is_valid():
#            u_form.save()
#            p_form.save()
#            #messages.success(request, f'Your account has been updated!')
#            return redirect('profile')  # Redirect back to profile page

#    else:
#        u_form = UserUpdateForm(instance=request.user)
#        p_form = ProfileUpdateForm(instance=request.user.profile)

#    context = {
#        'u_form': u_form,
#        'p_form': p_form
#    }

#    return render(request, 'account/profile.html', context)
