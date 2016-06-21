from streaming_dispatch.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm

from .models import Stream

def index(request):
    return render(request, 'index.html', {'streams': Stream.objects.all().order_by('-start')})

def stream(request, stream_id):
    return HttpResponse('haha ' + str(stream_id))

class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/login/"
    template_name = "register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)

from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import login

class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "login.html"

    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()

        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)

from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import logout

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")

# def create_stream(request):
