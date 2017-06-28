from django.forms.models import ModelForm

__author__ = 'hamid'

from django import forms
from .models import MyUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AbstractUser

class SendMessageForm(ModelForm):

    class Meta:
        model = MyUser
        fields = ('username', 'first_name', 'last_name',
                  'password1', 'password2',)
