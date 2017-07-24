from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView
from django_ajax.decorators import ajax
from django_ajax.mixin import AJAXMixin
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from authsystem.serializers import MyUserSerializer
from .models import MyUser
from rest_framework import generics
from .forms import SignUpForm
# Create your views here.


class SignupView(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'authsystem/signup.html'

    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    # success_url = reverse_lazy('authsystem:login')
    def get(self, request, *args, **kwargs):
        return Response()

    def post(self, request, *args, **kwargs):
        print(request.data)
        return Response()

    # def post(self, request, *args, **kwargs):
    #     print("here")
    #     print(request)
    #     super.post(self, request, *args, **kwargs)

