# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.contrib.auth.decorators import login_required
from django.core.serializers import json
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from datetime import datetime
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
import json
from rest_framework.response import Response
from authsystem.models import MyUser

from messaging.forms import CreateGroupForm
from messaging.serializers import MessageSerializer
from .models import Group, Message


@method_decorator(login_required, name='dispatch')
class ProfileView(ListView):
    model = Group
    template_name = 'messaging/profile.html'
    context_object_name = 'all_groups'


# @method_decorator(login_required, name='dispatch')
# class GroupView(CreateView):
#     model = Message
#     template_name = 'messaging/group.html'
#     context_object_name = 'message'
#     form_class = MessageForm
#
#     def get_template_names(self):
#         gp = Group.objects.get(pk=self.kwargs['group_id'])
#         members = gp.members.all()
#         if self.request.user in members:
#             return ['messaging/group.html']
#         else:
#             return ['messaging/group_not_joined.html']
#
#     def get_success_url(self):
#         return reverse('messaging:group', args=self.kwargs['group_id'])
#
#     def get_context_data(self, **kwargs):
#         context = super(GroupView, self).get_context_data(**kwargs)
#         gp = Group.objects.get(pk=self.kwargs['group_id'])
#         members = gp.members.all()
#         context['group'] = gp
#         if self.request.user in members:
#             context["message"] = self.model.objects.filter(group=gp)
#         return context
#
#     def form_valid(self, form):
#         gp = Group.objects.get(pk=self.request.POST.get("group_id"))
#         timezone.activate(settings.TIME_ZONE)
#         if gp.members.filter(id=self.request.user.id):
#             form.instance.author = self.request.user
#             temp = self.request.POST.get("group_id")
#             form.instance.group_id = temp
#             form.instance.date = timezone.localtime(timezone.now())
#             print(form.instance.date.strftime("%H:%M"))
#             self.object = form.save()
#             return HttpResponseRedirect(self.get_success_url())
#         raise PermissionDenied

class GroupView(generics.ListCreateAPIView):
    model = Message
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'messaging/group.html'

    def post(self, request, *args, **kwargs):
        print(request.data)
        msg = Message.objects.create(author=self.request.user,
                                     text=request.data['text'],
                                     group=Group.objects.get(pk=self.request.POST.get("group")),
                                                             date=timezone.localtime(timezone.now()))
        msg.save()

        return Response(MessageSerializer(msg).data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        group=Group.objects.get(pk=self.request.data["group"]),
                        date=timezone.localtime(timezone.now()))

    def get_queryset(self):
        return Message.objects.filter(group=Group.objects.get(pk=self.kwargs["group_id"]))

    def list(self, *args, **kwargs):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = MessageSerializer(queryset, many=True)
        to_return = []
        for item in serializer.data:
            temp = dict(item)
            temp['date'] = timezone.localtime(timezone.make_aware(datetime.strptime(temp['date'],
                                             "%Y-%m-%dT%H:%M:%S.%fZ"), timezone=timezone.get_default_timezone())).strftime("%H:%M")
            print(temp['date'])
            temp['author'] = MyUser.objects.get(pk=temp['author']).username
            to_return.append(temp)
        to_return = {'message':to_return, 'group_id':self.kwargs['group_id']}
        return Response(to_return)


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
