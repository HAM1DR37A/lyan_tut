# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# import datetime

from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.utils import timezone
import pytz
from Lyan_Tutorial import settings
from authsystem.models import MyUser

# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=30, null=False, unique=True)
    creator = models.ForeignKey(MyUser, on_delete=models.PROTECT, related_name='created_groups')
    members = models.ManyToManyField(MyUser, related_name='joined_groups')
    image = models.ImageField(upload_to='group_pics/',
                              default='group_pics/no-img.jpg')
    last_msg_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        super(Group, self).save(*args, **kwargs)
        self.members.add(self.creator)

    def __str__(self):
        return self.name



class Message(models.Model):
    group = models.ForeignKey(Group, related_name='group_messages', on_delete=models.CASCADE)
    author = models.ForeignKey(MyUser)
    date = models.DateTimeField(default=timezone.now)
    text = models.TextField()

    def get_date(self):
        if self.date.date() == timezone.now().date():
            return timezone.localtime(self.date).strftime("%H:%M")
        else:
            return timezone.localtime(self.date).strftime("%b %d")

    def get_text(self):
        if len(self.text) > 45:
            return self.author.first_name + ": " + self.text[:45] + " ..."
        else:
            return self.author.first_name + ": " + self.text

    class Meta:
        get_latest_by = "date"
        ordering = ['date']



@receiver(post_save, sender=Message)
def message_save_handler(sender, instance, *args, **kwargs):
    if instance.date >= instance.group.last_msg_date:
        instance.group.last_msg_date = instance.date
        instance.group.save()
