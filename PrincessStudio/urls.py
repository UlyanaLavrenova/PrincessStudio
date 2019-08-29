"""PrincessStudio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from psb import views

app_name = 'pbs'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^pbs/$', views.index),
    url(r'^pbs/register/$', views.RegisterFormView.as_view()),
    url(r'^pbs/login/$', views.LoginFormView.as_view()),
    url(r'^pbs/logout/$', views.LogoutView.as_view()),
    url(r'^pbs/password-change/', views.PasswordChangeView.as_view()),
    url(r'^pbs/vacant_dates/(?P<procedure_id>\d+)/$', views.vacant_dates),
    url(r'^pbs/vacant_dates/(?P<procedure_id>\d+)/selected_dates/cancel_record/(?P<record_id>\d+)$', views.cancel_record),
    url(r'^pbs/vacant_dates/(?P<procedure_id>\d+)/cancel_record/(?P<record_id>\d+)/', views.cancel_record),
    url(r'^pbs/vacant_dates/(?P<procedure_id>\d+)/(?P<vacant_times_id>\d+)/', views.record),
    url(r'^pbs/vacant_dates/(?P<procedure_id>\d+)/selected_dates/(?P<vacant_times_id>\d+)$', views.record),
    url(r'^pbs/vacant_dates/(?P<procedure_id>\d+)/selected_dates/', views.selected_date),
    url(r'^pbs/vacant_dates/(?P<procedure_id>\d+)/post/$', views.post, name='post'),
    url(r'^pbs/vacant_dates/(?P<procedure_id>\d+)/msg_list/$', views.msg_list, name='msg_list'),
]
