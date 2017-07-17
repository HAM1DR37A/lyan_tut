# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseRedirect, HttpResponse
from django.urls.base import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from Lyan_Tutorial import settings
from messaging.forms import CreateGroupForm, MessageForm
from .models import Group, Message


@method_decorator(login_required, name='dispatch')
class ProfileView(ListView):
    model = Group
    template_name = 'messaging/profile.html'
    context_object_name = 'all_groups'


@method_decorator(login_required, name='dispatch')
class GroupView(CreateView):
    model = Message
    template_name = 'messaging/group.html'
    context_object_name = 'message'
    form_class = MessageForm

    def get_template_names(self):
        gp = Group.objects.get(pk=self.kwargs['group_id'])
        members = gp.members.all()
        if self.request.user in members:
            return ['messaging/group.html']
        else:
            return ['messaging/group_not_joined.html']

    def get_success_url(self):
        return reverse('messaging:group', args=self.kwargs['group_id'])

    def get_context_data(self, **kwargs):
        context = super(GroupView, self).get_context_data(**kwargs)
        gp = Group.objects.get(pk=self.kwargs['group_id'])
        members = gp.members.all()
        context['group'] = gp
        if self.request.user in members:
            context["message"] = self.model.objects.filter(group=gp)
        return context

    def form_valid(self, form):
        gp = Group.objects.get(pk=self.request.POST.get("group_id"))
        timezone.activate(settings.TIME_ZONE)
        if gp.members.filter(id=self.request.user.id):
            form.instance.author = self.request.user
            temp = self.request.POST.get("group_id")
            form.instance.group_id = temp
            form.instance.date = timezone.localtime(timezone.now())
            print(form.instance.date.strftime("%H:%M"))
            self.object = form.save()
            return HttpResponseRedirect(self.get_success_url())
        raise PermissionDenied


@method_decorator(login_required, name='dispatch')
class CreateGroupView(CreateView):
    model = Group
    template_name = 'messaging/create_group.html'
    form_class = CreateGroupForm

    def get_success_url(self):
        return reverse('messaging:profile')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        super(CreateGroupView, self).form_valid(form)
        self.object.members.add(self.request.user)
        self.object.save() #TODO: Refactor this
        return HttpResponseRedirect(self.get_success_url())


@login_required
def join_group(request):
    if request.method == 'POST': #TODO: Refactor
        temp = request.POST.get("group_id")
        gp = Group.objects.get(pk=temp)
        members = gp.members.all()
        if request.user not in members:
            gp.members.add(request.user)
    return HttpResponseRedirect(reverse('messaging:profile'))
