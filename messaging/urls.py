__author__ = 'hamid'


from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'messaging'
urlpatterns = [
    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
    url(r'^(?P<group_id>[0-9])/group/$', views.GroupView.as_view(),
        name='group'),
    url(r'^send/$', views.GroupView.as_view(), name='send')
]