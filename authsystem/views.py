from django.urls.base import reverse_lazy
from django.views.generic.edit import CreateView
from .models import MyUser
from .forms import SignUpForm
# Create your views here.


class SignupView(CreateView):
    template_name = 'authsystem/signup.html'
    model = MyUser
    form_class = SignUpForm
    success_url = reverse_lazy('authsystem:login')
