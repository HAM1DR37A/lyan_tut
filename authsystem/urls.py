__author__ = 'hamid'

from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'authsystem'
urlpatterns = [
    url(r'^login/$', auth_views.login,
        {'template_name': 'authsystem/login.html'},  name='login'),
    url(r'^signup/$', views.SignupView.as_view(), name='signup'),
    url(r'^logout/$', auth_views.logout, {'next_page': "authsystem:login"},
        name='logout'),
]