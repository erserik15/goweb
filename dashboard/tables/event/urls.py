from django.urls import path
from . import views

urlpatterns = [
    path('event',views.EventListView.as_view(), name='event_index'),
    path('event/create', views.event_create, name='event_create'),
    path('event/update/<int:pk>', views.event_edit, name='event_edit'),
    path('event/delete/<int:pk>', views.event_delete, name='event_delete'),
]