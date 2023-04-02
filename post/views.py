from django.shortcuts import render
from django.http import HttpResponse

def post_index(request):
    return render(request, 'post/index.html')
