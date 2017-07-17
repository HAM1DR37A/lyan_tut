__author__ = 'hamid'


from django.conf.urls import url
from . import views

app_name = 'messaging'
urlpatterns = [
    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
    url(r'^(?P<group_id>[0-9])+/group/$', views.GroupView.as_view(),
        name='group'),
    url(r'^create_group/$', views.CreateGroupView.as_view(),
        name='create-group'),
    url(r'^join_group/$', views.join_group, name='join-group'),

]
