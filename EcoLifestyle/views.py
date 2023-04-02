from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'main/index.html')


def calendar(request):
    return render(request, 'calendar/index.html')


def calculator(request):
    if request.method == 'POST':
        response_data = {}
        for key, value in request.POST.items():
            response_data[key] = value
        return render(request, 'main/calendar.html')
    return render(request, 'calculator/index.html')


def blog(request):
    return render(request, 'blog.html')
