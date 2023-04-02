from django.shortcuts import render
from django.http import HttpResponse


def home(request):

    return render(request, 'index.html')


def calendar(request):

    return render(request, 'calendar.html')


def calculator(request):
    if request.method == 'POST':
        response_data = {}
        
        for key, value in request.POST.items():
            response_data[key] = value
        print(str(response_data))
        return render(request, 'calendar.html')
    return render(request, 'calculator.html')


def blog(request):

    return render(request, 'blog.html')
