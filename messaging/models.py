# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from authsystem.models import MyUser

# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=30, null=False, default='Group')
    creator = models.ForeignKey(MyUser, on_delete=models.PROTECT, related_name='creator')
    members = models.ManyToManyField(MyUser, related_name='members')

    def __str__(self):
        return self.name


class Message(models.Model):
    group = models.ForeignKey(Group)
    author = models.ForeignKey(MyUser)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()