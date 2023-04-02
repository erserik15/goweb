from django.urls import path
from . import views

urlpatterns = [
    path('volunteer_request',views.VolunteerRequestListView.as_view(), name='volunteer_request_index'),
    path('volunteer_request/create', views.volunteer_request_create, name='volunteer_request_create'),
    path('volunteer_request/update/<int:pk>', views.volunteer_request_edit, name='volunteer_request_edit'),
    path('volunteer_request/delete/<int:pk>', views.volunteer_request_delete, name='volunteer_request_delete'),
]