import imp
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

CHOICES = (
    ('student', 'STUDENT'),
    ('tutor', 'TUTOR'),   
    )

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    #fname = forms.CharField(max_length=25)
    #lname = forms.CharField(max_length=25)
    first_name = forms.CharField(max_length=25)
    last_name = forms.CharField(max_length=25)
    #account_type = forms.CharField(label='Select', widget=forms.Select(choices=CHOICES))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']



class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email']



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'country', 'city', 'bio', 'account_Type', 'github', 'twitter', 'linkedin', 'facebook', 'instagram']