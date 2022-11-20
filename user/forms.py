from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import Profile
from user.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, help_text='Required. Add a valid email address.')

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2', )

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = User.objects.exclude(
                pk=self.instance.pk).get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = User.objects.exclude(
                pk=self.instance.pk).get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            'Username "%s" is already in use.' % username)


class AccountAuthenticationForm(forms.ModelForm):

    email = forms.CharField()
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']

            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")


class UserUpdateForm(forms.ModelForm):
    # email = forms.EmailField()
    class Meta:
        model = User
        fields = ['profile_image']
        fields = ['username','email']

# Create a ProfileUpdateForm to update image
class ProfileUpdateForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-group'}))
    class Meta:
        model = Profile
        fields = ['image']
