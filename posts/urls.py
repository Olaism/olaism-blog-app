from django.urls import path

from .views import (
    PostListView, 
    PostDetailView,
    PostUpdateView,
    PostCreateView,
    PostDeleteView
)

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('new/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name="post_update"),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name="post_delete")
]