from django.urls import path
from . import views

urlpatterns = [
    path('user',views.UserListView.as_view(), name='user_index'),
    path('user/create', views.user_create, name='user_create'),
    path('user/update/<int:pk>', views.user_edit, name='user_edit'),
    path('user/delete/<int:pk>', views.user_delete, name='user_delete'),
]