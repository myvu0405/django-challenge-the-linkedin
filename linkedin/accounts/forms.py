from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import *

class UserRegisterForm(UserCreationForm):
    class Meta:
        model=LinkedinUser
        fields = ['email','name','job_title','password1','password2']

class MemberForm(forms.ModelForm):

    class Meta:
        model=LinkedinUser
        fields='__all__'