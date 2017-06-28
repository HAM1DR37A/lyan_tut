from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.urls.base import reverse, reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from .models import MyUser
from .forms import SignUpForm
# Create your views here.


class SignupView(CreateView):
    template_name = 'authsystem/signup.html'
    model = MyUser
    form_class = SignUpForm
    success_url = reverse_lazy('authsystem:login')