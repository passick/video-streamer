from streaming_dispatch.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime

from utils import *

from .models import Stream

def index(request):
    streams = []
    username = request.GET.get('by')
    if username:
        try:
            user = User.objects.get(username=username)
            streams = user.stream_set.all().order_by('-start')
        except User.DoesNotExist:
            return redirect('index')
    else:
        streams = Stream.objects.all().order_by('-start')
    return render(request, 'index.html',
            {'streams': streams,
             'show_create_stream_link': request.user.is_authenticated
            })

def stream(request, stream_id):
    requested_stream = get_object_or_404(Stream, id=stream_id)
    is_author = (request.user == requested_stream.author)
    return render(request, 'stream.html',
            {'stream': requested_stream, 'is_author': is_author})

@login_required
def create_stream(request):
    if request.method == 'POST':
        form = StreamForm(request.POST)
        if form.is_valid():
            stream = form.save(commit=False)
            stream.active = False
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

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@csrf_exempt
def stream_status_changed(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("You should POST.")
    server_ip = get_client_ip(request)
    if not StreamingServer.objects.filter(url=server_ip).exists():
        return HttpResponseForbidden("")
    stream_id = request.POST['name']
    if not stream_id:
        return HttpResponseBadRequest("Need id.")
    try:
        stream_id = int(stream_id)
        status = int(request.POST['status'])
        stream = Stream.objects.get(id=stream_id)
        if status == 0:
            stream.active = False
        else:
            stream.active = True
        stream.save()
        return HttpResponse("ok")
    except ValueError:
        return HttpResponseBadRequest("Need valid id and new status.")

class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/"
    template_name = "register.html"

    def form_valid(self, form):
        form.save()
        new_user = authenticate(username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'])
        login(self.request, new_user)
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
