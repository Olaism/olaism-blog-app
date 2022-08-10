from django.urls import path

from .views import (
    PostListView, 
    PostDetailView,
    PostUpdateView,
    PostCreateView,
    PostDeleteView,
    MyPostsView,
    publish_post,
)

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('new/', PostCreateView.as_view(), name='post_create'),
    path('my-post/', MyPostsView.as_view(), name='my_posts'),
    path('<int:pk>/publish/', publish_post, name='publish_post'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name="post_update"),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name="post_delete")
]