from django.conf.urls import url, include

from . import views

urlpatterns = [
        url(r'^register/$', views.RegisterFormView.as_view()),
        url(r'^login/$', views.LoginFormView.as_view()),
        url(r'^accounts/login/$', views.LoginFormView.as_view()),
        url(r'^logout/$', views.LogoutView.as_view()),
        url(r'^create_stream/$', views.create_stream, name='create_stream'),
        url(r'^$', views.index, name='index'),
        url(r'^stream/(?P<stream_id>[0-9]+)/', views.stream, name='stream'),
        # url(r'^login', 'django.contrib.auth.views.login'),
        # url(r'^logout/$', views.logout_page),
        # url(r'^accounts/', include('registration.backends.simple.urls')),
        # url(r'^accounts/login/$', 'django.contrib.auth.views.login'), # If user is not login it will redirect to login page
        # url(r'^register/$', views.register),
        # url(r'^home/$', views.home),
        ]
