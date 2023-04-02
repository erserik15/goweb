from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('calendar', calendar, name='home'),
    path('calculator', calculator, name='home'),
    path('blog', blog, name='home'),
]