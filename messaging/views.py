# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect

from django.shortcuts import render

# Create your views here.
from django.urls.base import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from .models import Group, Message


@method_decorator(login_required, name='dispatch')
class ProfileView(ListView):
    model = Group
    template_name = 'messaging/profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ListView, self).get_context_data(*args, **kwargs)
        context['all_groups'] = Group.objects.all()
        context['created_groups'] = Group.objects.\
            filter(creator=self.request.user)
        context['my_groups'] = Group.objects.filter(members=self.request.user)
        return context

@method_decorator(login_required, name='dispatch')
class GroupView(CreateView):
    model=Message
    template_name = 'messaging/group.html'
    context_object_name = 'message'
    fields = ['text']

    def get_success_url(self):
        return reverse('messaging:group', args=self.kwargs['group_id'])

    def get_context_data(self, **kwargs):
        context = super(GroupView, self).get_context_data(**kwargs)
        gp = Group.objects.get(pk=self.kwargs['group_id'])
        context["message"] = self.model.objects.filter(group=gp)
        context['group_id'] = self.kwargs['group_id']
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        temp = self.request.POST.get("group_id")
        temp = int(temp[:len(temp)-1])
        form.instance.group_id = temp
        super(GroupView, self).form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

# @login_required
# def send(request, group_id, message_text):
#     if request.method == "POST":
#         usr = request.user
#         Message.objects.create(group=Group.objects.get(pk=group_id), author=usr, text=message_text)
#     return HttpResponseRedirect(reverse('messaging:group', args=(group_id,)))



