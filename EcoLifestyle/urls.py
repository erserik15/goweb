from django.urls import path
from .views import *

app_name='ecolifestyle'
urlpatterns = [
    path('', home, name='home'),
    path('calendar', calendar, name='calendar'),
    path('calculator', calculator, name='calculator'),
]