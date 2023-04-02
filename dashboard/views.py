# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, get_object_or_404

from ecolifestyle.models import *


@login_required()
def welcome(request):
    context = {'segment': 'welcome'}
    html_template = loader.get_template('dashboard/welcome.html')
    return HttpResponse(html_template.render(context, request))

@login_required()
def profile(request):
    context = {'segment': 'profile'}
    html_template = loader.get_template('dashboard/profile.html')
    return HttpResponse(html_template.render(context, request))


@login_required()
def pages(request):
    context = {}
    html_template = loader.get_template('dashboard/page-404.html')
    return HttpResponse(html_template.render(context, request))
    # try:

    #     load_template = request.path.split('/')[-1]

    #     if load_template == 'admin':
    #         return HttpResponseRedirect(reverse('admin:index'))
    #     context['segment'] = load_template

    #     html_template = loader.get_template('dashboard/' + load_template)
    #     return HttpResponse(html_template.render(context, request))

    # except template.TemplateDoesNotExist:

    #     html_template = loader.get_template('dashboard/page-404.html')
    #     return HttpResponse(html_template.render(context, request))

    # except:
    #     html_template = loader.get_template('dashboard/page-500.html')
    #     return HttpResponse(html_template.render(context, request))

