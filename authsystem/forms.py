__author__ = 'hamid'

from .models import MyUser
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Re-Password'


    class Meta:
        model = MyUser
        fields = ('username', 'first_name', 'last_name',
                  'password1', 'password2',)
