from streaming_dispatch.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime

from utils import *

from .models import Stream

def index(request):
    return render(request, 'index.html', {'streams': Stream.objects.all().order_by('-start')})

def stream(request, stream_id):
    requested_stream = get_object_or_404(Stream, id=stream_id)
    is_author = (request.user == requested_stream.author)
    return render(request, 'stream.html',
            {'stream': requested_stream,
                'is_author': is_author,
                'dash_url': get_dash_stream_url(requested_stream),
                'viewer_url': get_stream_viewer_url(requested_stream),
                'publisher_url': get_stream_publisher_url(requested_stream)})

@login_required
def create_stream(request):
    if request.method == 'POST':
        form = StreamForm(request.POST)
        if form.is_valid():
            stream = form.save(commit=False)
            stream.active = True
            stream.author = request.user
            stream.start = datetime.now()
            stream.save()
            if not push_stream_to_server(stream):
                stream.delete()
                return HttpResponse('Could not connect to streaming server')
            return redirect('stream', stream_id=stream.id)
    else:
        form = StreamForm()
    return render(request, 'add_stream.html', {'form': form})

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
