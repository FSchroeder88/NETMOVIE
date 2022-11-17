from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from user.forms import RegistrationForm, AccountAuthenticationForm
from .models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site  
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.utils.encoding import force_bytes, force_str  
from .token import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from .forms import  UserUpdateForm, ProfileUpdateForm
from django.contrib import messages

def home(request):
    return render(request, 'home.html')    

def register_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse("You are already authenticated as " + str(user.email))

    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            #form.save()
            # save form in the memory not in database 
            user = form.save(commit=False)  
            user.is_active = False  
            user.save() 

            # to get the domain of the current site
            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email id' 
            message = render_to_string('acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()  
            return HttpResponse('Please confirm your email address to complete the registration')

            # email = form.cleaned_data.get('email').lower()
            # raw_password = form.cleaned_data.get('password')
            # account = authenticate(email=email, password=raw_password)
            # login(request, account)
            # destination = kwargs.get("next")
            # if destination:
            #     return redirect(destination)
            # return redirect('login')

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'register.html', context)


def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:  
        return HttpResponse('Activation link is invalid!')      


def logout_view(request):
    logout(request)
    return redirect('login')


def login_view(request, *args, **kwargs):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('video')

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
                return redirect('video')

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form

    return render(request, 'login.html', context)


def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
    return redirect


@login_required  # Require user logged in before they can access profile page
def profile_view(request):
   if request.method == 'POST':
       u_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
       p_form = ProfileUpdateForm(request.POST, request.FILE, instance=request.user.profile)
       if u_form.is_valid() and p_form.is_valid():
           u_form.save()
           p_form.save()
           messages.success(request, f'Your account has been updated!')
           return redirect(to='profile')  # Redirect back to profile page

   else:
       u_form = UserUpdateForm(instance=request.user)
       p_form = ProfileUpdateForm(instance=request.user.profile)

   context = {
       'u_form': u_form,
       'p_form': p_form
   }

   return render(request, 'profile.html', context)
