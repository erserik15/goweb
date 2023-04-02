from django.urls import path
from . import views

urlpatterns = [
    path('post',views.PostListView.as_view(), name='post_index'),
    path('post/create', views.post_create, name='post_create'),
    path('post/update/<int:pk>', views.post_edit, name='post_edit'),
    path('post/delete/<int:pk>', views.post_delete, name='post_delete'),
]