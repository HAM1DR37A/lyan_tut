__author__ = 'hamid'

from django import forms
from .models import MyUser
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):

    class Meta:
        model = MyUser
        fields = ('username', 'first_name', 'last_name',
                  'password1', 'password2',)
