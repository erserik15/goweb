from django.urls import path, re_path, include
from . import views

app_name = 'post'

urlpatterns = [
    path('', views.post_index, name='index'),
]
