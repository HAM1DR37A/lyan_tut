from django.forms.models import ModelForm
from django.utils import timezone
from Lyan_Tutorial import settings

__author__ = 'hamid'

from .models import Group, Message


class CreateGroupForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Group Name'

    class Meta:
        model = Group
        fields = ('name', 'image',)


class MessageForm(ModelForm):
    def __init__(self, *args, **kwargs):
        timezone.activate(settings.TIME_ZONE)
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['placeholder'] = 'Type here to send a message'


    class Meta:
        model = Message
        fields = ('text', )
