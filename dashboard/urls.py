# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path, include
from dashboard import views


app_name = 'dashboard'

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('welcome', views.welcome, name='welcome'),
    path('profile', views.profile, name='profile'),
    path('', include('dashboard.tables.event.urls')),
    path('', include('dashboard.tables.user.urls')),
    path('', include('dashboard.tables.post.urls')),
    path('', include('dashboard.tables.volunteer_request.urls')),
    path('pages', views.pages, name='pages'),
]
